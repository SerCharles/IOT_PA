import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math


def moving_average(wave_y, window):
    '''
    描述：滑动平均
    参数：波y，窗口大小
    返回：滤波结果
    '''
    N = wave_y.shape[0]
    M = N - window + 1
    result_y = np.zeros(M)
    for i in range(M):
        sum = 0
        for j in range(window):
            sum += wave_y[i + j]
        average = sum / window
        result_y[i] = average
    return result_y

def bandpass(x, y):
    '''
    描述：带通滤波
    参数：波x, y
    返回：滤波结果
    '''
    n_frames = x.shape[0]
    sample_time = (x[n_frames - 1] - x[0]) / (n_frames - 1)
    framerate = 1 / sample_time
    low_1 = 2 * 17000 / framerate
    high_1 = 2 * 18000 / framerate
    low_2 = 2 * 20000 / framerate
    high_2 = 2 * 21000 / framerate

    b_1, a_1 = signal.butter(8, [low_1, high_1], 'bandpass')
    b_2, a_2 = signal.butter(8, [low_2, high_2], 'bandpass')

    filter_1 = signal.filtfilt(b_1, a_1, y) 
    filter_2 = signal.filtfilt(b_2, a_2, y)
    return filter_1, filter_2 