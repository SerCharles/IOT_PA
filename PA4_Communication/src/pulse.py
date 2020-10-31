import numpy as np
from scipy import signal
from utils import bandpass, FFT, moving_average




def generate_pulse(framerate, frequency, volume, start_place, duration):
    '''
    描述：生成脉冲信号
    参数：帧率，频率，振幅，相位，时长
    返回：波形
    '''
    n_frames = round(duration * framerate)
    x = np.linspace(0, duration, num = n_frames)
    y = np.sin(2 * np.pi * frequency * x + start_place) * volume
    return y

def generate_empty(framerate, duration):
    '''
    描述：生成空白信号
    参数：帧率，时长
    返回：波形
    '''
    n_frames = round(duration * framerate)
    x = np.linspace(0, duration, num = n_frames)
    y = np.zeros(x.shape)
    return y

def get_pulse_max(pulse, window, volume):
    '''
    描述：获取脉冲极大值位置
    参数：脉冲，窗口大小， 振幅
    返回：极大值位置列表
    '''
    max_list = []
    n_frames = pulse.shape[0]
    threshold = 0.3 * volume
    for i in range(n_frames - window + 1):
        max_num = max(pulse[i: i + window])
        middle_num = i + window // 2
        if pulse[middle_num] >= max_num and pulse[middle_num] > threshold:
            max_list.append(middle_num)
    return max_list

def pulse_modulation(seq, args):
    '''
    描述：脉冲调制, 参数列表
    参数：0-1序列
    返回：调制后的信号
    '''
    framerate = args.framerate
    frequency = args.frequency
    volume = args.volume
    start_place = args.start_place
    pulse_length = args.pulse_length
    interval_0 = args.interval_0
    interval_1 = args.interval_1
    y = np.empty(shape = (1, 0))
    for item in seq:
        pulse = generate_pulse(framerate, frequency, volume, start_place, pulse_length)
        if item == 0:
            empty = generate_empty(framerate, interval_0)
        elif item == 1:
            empty = generate_empty(framerate, interval_1)
        y = np.append(y, pulse)
        y = np.append(y, empty)
    pulse = generate_pulse(framerate, frequency, volume, start_place, pulse_length)
    y = np.append(y, pulse)
    return y

def pulse_demodulation(y, args):
    '''
    描述：脉冲解调
    参数：信号，参数列表
    返回：返回：0-1序列
    '''
    framerate = args.framerate
    frequency = args.frequency
    volume = args.volume
    start_place = args.start_place
    pulse_length = args.pulse_length
    interval_0 = args.interval_0
    interval_1 = args.interval_1
    duration_pulse = round(pulse_length * framerate)
    duration_0 = round(interval_0 * framerate)
    duration_1 = round(interval_1 * framerate)

    window = duration_pulse
    seq = []
    y = bandpass(y, framerate, frequency - 500, frequency + 500) #先滤波
    y = FFT(y, window, framerate, frequency) #fourier变换
    y = moving_average(y)
    max_list = get_pulse_max(y, window, volume)

    previous = 0
    for i in range(len(max_list)):
        duration = max_list[i] - previous - duration_pulse
        if duration >= duration_0 * 0.9 and duration <= duration_0 * 1.1:
            seq.append(0)
        else: 
            seq.append(1)
        previous = max_list[i]
    return seq

