import numpy as np
import matplotlib.pyplot as plt
import math
import wave
from scipy.io import wavfile
import struct

def constant_wave(N):
    my_x = np.zeros(N)
    my_wave = np.zeros(N)
    for i in range(N):
        my_x[i] = i
        my_wave[i] = 1
    return my_x, my_wave


def linear_wave(N):
    my_x = np.zeros(N)
    my_wave = np.zeros(N)
    for i in range(N):
        my_x[i] = i
        my_wave[i] = 1 - abs(i) / N
    return my_x, my_wave

def sine_wave(N):
    my_x = np.zeros(N)
    my_wave = np.zeros(N)
    for i in range(N):
        my_x[i] = i
        my_wave[i] = math.sin(2 * math.pi * i / N)
    return my_x, my_wave

def load_wave(save_dir = 'sound.wav'):
    file = wave.open(save_dir)
    for item in enumerate(file.getparams()):
        print(item)
    n_frames = file.getparams().nframes  # 帧总数
    framerate = file.getparams().framerate  # 采样频率
    sample_time = 1 / framerate  # 采样点的时间间隔
    duration = n_frames / framerate  # 声音信号的长度
    frequency, audio_sequence = wavfile.read(save_dir)
    x_seq = np.arange(0, duration, sample_time)
    return x_seq, audio_sequence

def plot_wave(x, y):
    plt.plot(x, y, 'blue')
    plt.xlabel("time")
    plt.show()

def plot_frequency(frequency, amp):
    plt.plot(frequency, amp, 'blue')
    plt.xlabel("frequency")
    plt.show()

def plot_comparison(x, y, amplitude_np, spectrum_np, amplitude_mine, spectrum_mine):
    plt.suptitle("Plot wave and its DFT")
    plt.subplots_adjust(hspace = 0.6, wspace = 0.2)
    plt.subplot(3, 2, 1)
    plt.plot(x, y, 'blue')
    plt.title("the wave itself")

    plt.subplot(3, 2, 3)
    plt.plot(np.abs(amplitude_np))
    plt.title("amplitude by numpy")

    plt.subplot(3, 2, 5)
    plt.plot(np.abs(spectrum_np))
    plt.title("spectrum by numpy")

    plt.subplot(3, 2, 4)
    plt.plot(np.abs(amplitude_mine))
    plt.title("amplitude by myself")

    plt.subplot(3, 2, 6)
    plt.plot(np.abs(spectrum_mine))
    plt.title("spectrum by myself")
    plt.show()