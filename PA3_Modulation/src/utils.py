import wave
import os
import numpy as np
from scipy.io import wavfile
import struct
import matplotlib.pyplot as plt
from scipy import signal


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
        the_result = int(my_wave[i])
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
    return audio_sequence

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