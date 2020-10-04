import wave
import numpy as np
from scipy.io import wavfile
import struct
import matplotlib.pyplot as plt

def generate_wave(framerate = 44100, duration = 5, frequency = 2000, start_place = 0, volume = 1000, sample_width = 2, save_dir = 'sound.wav'):
    '''
    采样率，持续时间，频率，初始相位，音量
    '''
    x = np.linspace(0, duration, num=duration*framerate)
    y = np.sin(2 * np.pi * frequency * x + start_place) * volume
    # 将波形数据转换成数组
    sine_wave = y
    #save wav file
    wf = wave.open(save_dir, 'wb')
    wf.setnchannels(1)
    wf.setframerate(framerate)
    wf.setsampwidth(sample_width)
    for i in sine_wave:
        data = struct.pack('<h', int(i))
        wf.writeframesraw(data)
    wf.close()


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

    plt.plot(x_seq, audio_sequence, 'blue')
    plt.xlabel("time (s)")
    plt.show()

generate_wave(framerate = 200)
load_wave()