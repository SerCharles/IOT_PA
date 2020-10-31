import wave
import os
import argparse
import numpy as np
import random
from scipy.io import wavfile
import struct
import matplotlib.pyplot as plt
from scipy import signal

def encode(s):
    '''
    字符串转二进制
    '''
    a = []
    for i in s:
        the_ord = ord(i)
        if the_ord < 0 or the_ord >= 128:
            raise Exception
        a.append((the_ord >> 6) & 1)
        a.append((the_ord >> 5) & 1)
        a.append((the_ord >> 4) & 1)
        a.append((the_ord >> 3) & 1)
        a.append((the_ord >> 2) & 1)
        a.append((the_ord >> 1) & 1)
        a.append((the_ord >> 0) & 1)
    return a

 
def decode(s):
    '''
    二进制转字符串
    '''
    my_str = ''
    i = len(s)
    while i - 7 >= 0:
        current = s[i - 7: i]
        my_sum = current[0] * 64 + current[1] * 32 + current[2] * 16 + current[3] * 8 + current[4] * 4 + current[5] * 2 + current[6] * 1
        my_char = chr(my_sum)
        my_str += my_char
        i -= 7
    my_str = my_str[::-1]
    return my_str

def filt_wave(s):
    '''
    录音时去除振幅太小的部分
    '''
    new_s = []
    for item in s:
        if abs(item) >= 0.01:
            new_s.append(item)
    return new_s 


def init_params():
    '''
    描述：读取参数
    参数：无
    返回：无
    '''
    parser = argparse.ArgumentParser(description="Choose the parameters")
    parser.add_argument("--framerate", type = int, default = 48000)
    parser.add_argument("--frequency", type = int, default = 10000)
    parser.add_argument("--sample_width", type = int, default = 2)
    parser.add_argument("--nchannels", type = int, default = 1)
    parser.add_argument("--volume", type = float, default = 10000.0)
    parser.add_argument("--start_place", type = int, default = 0)
    parser.add_argument("--pulse_length", type = float, default = 0.01)
    parser.add_argument("--interval_0", type = float, default = 0.01)
    parser.add_argument("--interval_1", type = float, default = 0.02)
    parser.add_argument("--save_base_send", type = str, default = 'send')
    parser.add_argument("--save_base_receive", type = str, default = 'receive')
    args = parser.parse_args()
    return args

def save_wave(my_wave, framerate = 44100, sample_width = 2, nchannels = 1, save_base = 'sound', file_name = 'pulse.wav'):
    '''
    描述：存储wav文件
    参数：波，帧率，采样宽度， 通道数，文件夹名，文件名
    返回：无
    '''
    the_place = os.path.join(save_base, file_name)
    wf = wave.open(the_place, 'wb')
    wf.setnchannels(nchannels)
    wf.setframerate(framerate)
    wf.setsampwidth(sample_width)
    for i in range(len(my_wave)):
        the_result = int(my_wave[i]) #*/1000，否则信息会有丢失
        data = struct.pack('<h', the_result)
        wf.writeframesraw(data)
    wf.close()


def load_wave(save_base = 'sound', file_name = 'pulse.wav'):
    '''
    描述：读取wav文件
    参数：文件夹名，文件名, 帧数，帧率，采样时间，长度
    返回：y
    '''
    the_place = os.path.join(save_base, file_name)
    file = wave.open(the_place)
    n_frames = file.getparams().nframes  # 帧总数
    framerate = file.getparams().framerate  # 采样频率
    sample_time = 1 / framerate  # 采样点的时间间隔
    duration = n_frames / framerate  # 声音信号的长度

    frequency, audio_sequence = wavfile.read(the_place)
    x_seq = np.arange(0, duration, sample_time)
    print("n_frames:", n_frames)
    print("framerate:", framerate)
    print("sample_time:", sample_time)
    print("duration:", duration)
    print("frequency:", frequency)
    y = audio_sequence  #*/1000，否则信息会有丢失
    return y

def bandpass(y, framerate, low, high):
    '''
    描述：带通滤波
    参数：波, 采样率, 滤波频率上下界
    返回：滤波结果
    '''
    low = 2 * low / framerate
    high = 2 * high / framerate
    b, a = signal.butter(6, [low, high], 'bandpass')
    result = signal.filtfilt(b, a, y) 
    return result

def FFT(y, window, framerate, frequency):
    '''
    描述：对信号做滑动窗口FFT
    参数：信号y， 窗口大小， 帧率，频率
    返回：结果
    '''
    n_frames = y.shape[0]
    result = np.zeros(n_frames)
    for i in range(n_frames - window + 1):
        nova = abs(np.fft.fft(y[i: i + window]))
        #得到目标频率傅里叶变换结果中对应的index
        index_impulse = round(frequency / framerate * window);
        #考虑到声音通信过程中的频率偏移，我们取以目标频率为中心的5个频率采样点中最大的一个来代表目标频率的强度
        result[i] = max(nova[index_impulse - 2: index_impulse + 2]);
    return result

def moving_average(wave_y, window = 11):
    '''
    描述：对信号做滑动平均
    参数：波y，窗口大小
    返回：滤波结果
    '''
    N = wave_y.shape[0]
    M = N - window + 1
    result_y = np.zeros(M)
    for i in range(M):
        the_sum = 0
        for j in range(window):
            the_sum += wave_y[i + j]
        average = the_sum / window
        result_y[i] = average
    return result_y

def generate_random_seq(length):
    '''
    描述：生成随机0-1序列
    参数：长度
    返回：随机0-1序列
    '''
    original_seq = []
    for i in range(length):
        num = round(random.random())
        original_seq.append(num)
    return original_seq

def fill_seq(seq):
    '''
    描述：如果seq长度不是偶数，补0
    参数：原先seq
    返回：新seq
    '''
    if len(seq) % 2 == 0:
        return seq
    else: 
        seq.append(0)
        return seq

def compare_seqs(original_seq, get_seq):
    '''
    描述：比较两个seq是否一样
    参数：原先和获取的seq
    返回：正确/错误
    '''
    if len(original_seq) != len(get_seq):
        return False
    for i in range(len(original_seq)):
        if original_seq[i] != get_seq[i]:
            return False
    return True

def get_success_rate(original_seq, get_seq):
    '''
    描述：计算传输准确率
    参数：原先和获取的seq
    返回：准确率
    '''
    low_len = min(len(original_seq), len(get_seq))
    correct_num = 0
    for i in range(low_len):
        if original_seq[len(original_seq) - i] == get_seq[len(get_seq) - i]:
            correct_num += 1
    accuracy = correct_num / len(original_seq)
    return accuracy