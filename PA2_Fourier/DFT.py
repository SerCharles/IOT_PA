import numpy as np
import matplotlib.pyplot as plt
import math

def DFT(N,  wave_y):
    '''
    描述：DFT
    参数：采样点个数N，波的y
    返回：频谱的amplitude, spectrum
    '''
    amplitude_list = np.zeros(N, dtype = complex)
    spectrum_list = np.zeros(N)

    for i in range(N):
        for j in range(N):
            param = wave_y[j]
            base = 2 * math.pi * i * j / N
            
            result_base = complex(math.cos(base), math.sin(base))
            amplitude = result_base * param
            amplitude_list[i] += amplitude
    for i in range(N):
        spectrum_list[i] = amplitude_list[i] ** 2
    return amplitude_list, spectrum_list






