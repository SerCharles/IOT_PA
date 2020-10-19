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
    n_frames = file.getparams().nframes  # 帧总数
    framerate = file.getparams().framerate  # 采样频率
    sample_time = 1 / framerate  # 采样点的时间间隔
    duration = n_frames / framerate  # 声音信号的长度

    frequency, audio_sequence = wavfile.read(save_dir)
    x_seq = np.arange(0, duration, sample_time)
    print("n_frames:", n_frames)
    print("framerate:", framerate)
    print("sample_time:", sample_time)
    print("duration:", duration)
    print("frequency:", frequency)
    return x_seq, audio_sequence

def add_zero(x, y):
    n_frames = x.shape[0]
    sample_time = (x[n_frames - 1] - x[0]) / (n_frames - 1)
    duration = n_frames * sample_time
    new_duration = duration * 10
    new_x = np.arange(0, new_duration, sample_time)
    new_y = np.zeros(n_frames * 10)
    for i in range(n_frames):
        new_y[i] = y[i]
    return new_x, new_y

def plot_frequency(amp):
    plt.plot(amp, 'blue')
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

def plot_filter(x, amplitude_old, spectrum_old, amplitude_new, spectrum_new):
    n_frames = x.shape[0]
    sample_time = (x[n_frames - 1] - x[0]) / (n_frames - 1)
    framerate = 1 / sample_time
    old_x = np.arange(0, framerate, framerate / n_frames)[: n_frames]
    new_x = np.arange(0, framerate, framerate / amplitude_new.shape[0])[:amplitude_new.shape[0]]
    print(amplitude_new.shape[0], new_x.shape)

    plt.suptitle("Plot old wave and new wave")
    plt.subplots_adjust(hspace = 0.6, wspace = 0.2)
    plt.subplot(2, 2, 1)
    plt.plot(old_x, np.abs(amplitude_old))
    plt.xlabel("frequency")
    plt.title("amplitude of original wave")

    plt.subplot(2, 2, 3)
    plt.plot(old_x, np.abs(spectrum_old))
    plt.xlabel("frequency")
    plt.title("spectrum of original wave")

    plt.subplot(2, 2, 2)
    plt.plot(new_x, np.abs(amplitude_new))
    plt.xlabel("frequency")
    plt.title("amplitude of filted wave")

    plt.subplot(2, 2, 4)
    plt.plot(new_x, np.abs(spectrum_new))
    plt.xlabel("frequency")
    plt.title("spectrum of filted wave")
    plt.show()