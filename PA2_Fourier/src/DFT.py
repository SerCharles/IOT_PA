import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math

def DFT(wave_y):
    '''
    描述：DFT
    参数：波的y
    返回：频谱的amplitude
    '''
    N = wave_y.shape[0]
    amplitude_list = np.zeros(N, dtype = complex)

    for i in range(N):
        for j in range(N):
            param = wave_y[j]
            base = 2 * math.pi * i * j / N
            
            result_base = complex(math.cos(base), math.sin(base))
            amplitude = result_base * param
            amplitude_list[i] += amplitude

    return amplitude_list

def STFT(wave_y, window):
    '''
    描述：DFT
    参数：波的y, 窗口大小
    返回：无
    '''
    fs = wave_y.shape[0]
    f, t, Zxx = signal.stft(wave_y, fs, nperseg = window)
    plt.pcolormesh(t, f, np.abs(Zxx))
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()





