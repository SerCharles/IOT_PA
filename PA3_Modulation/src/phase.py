import numpy as np
from math import *
from scipy import signal


def get_sequences(seq):
    '''
    描述：根据0-1序列获取i，q序列
    参数：输入的0-1序列
    返回：i序列，q序列
    '''
    seq_i = []
    seq_q = []
    i = 0
    while i < len(seq):
        if(i == len(seq)):
            item = seq[i]
        else: 
            item = seq[i] * 2 + seq[i + 1]
        if item == 0:
            seq_i.append(sqrt(2) / 2)
            seq_q.append(sqrt(2) / 2)
        elif item == 1:
            seq_i.append(sqrt(2) / 2)
            seq_q.append(-sqrt(2) / 2)
        elif item == 2:
            seq_i.append(-sqrt(2) / 2)
            seq_q.append(sqrt(2) / 2)
        elif item == 3:
            seq_i.append(-sqrt(2) / 2)
            seq_q.append(-sqrt(2) / 2)
        i += 2
    return seq_i, seq_q

def get_one_phase(i, q, frequency, framerate, interval, volume):
    '''
    描述：获取一个QPSK阶段结果
    参数：i, q, 频率，帧率，间隔，振幅
    返回：调制结果部分
    '''
    total_num = round(framerate * interval)
    x = np.linspace(0, interval, num = total_num)
    y_cos = np.cos(2 * np.pi * x * frequency) * volume
    y_sin = np.sin(2 * np.pi * x * frequency) * volume
    y = i * y_sin + q * y_cos
    return y

def phase_modulation(seq, args):
    '''
    描述：QPSK调制
    参数：0-1序列，参数
    返回：调制结果波
    '''
    framerate = args.framerate
    frequency = args.frequency
    volume = args.volume
    start_place = args.start_place
    interval = args.interval

    seq_i, seq_q = get_sequences(seq)
    y = np.empty(shape = (1, 0))
    for i in range(len(seq_i)):
        new_y = get_one_phase(seq_i[i], seq_q[i], frequency, framerate, interval, volume)
        y = np.append(y, new_y)
    return y

def get_integral(type, sub_seq, frequency, framerate, interval, volume):
    '''
    描述：计算一个间隔中的积分
    参数：积分类型（cos，sin），波的子序列，频率，帧率，间隔，振幅
    返回：积分数值
    '''
    the_sum = 0
    total_num = len(sub_seq)
    x = np.linspace(0, total_num / framerate, num = total_num)
    if type == 'cos':
        y = np.cos(2 * np.pi * x * frequency) * volume
    else: 
        y = np.sin(2 * np.pi * x * frequency) * volume
    for i in range(total_num):
        the_sum += sub_seq[i] * y[i] / framerate
    return the_sum

def get_original_seq(seq_i, seq_q):
    '''
    描述：根据i，q序列还原原先的0-1序列
    参数：i，q序列
    返回：0-1序列
    '''
    seq = []
    for i in range(len(seq_i)):
        if seq_i[i] > 0 and seq_q[i] > 0:
            seq.append(0)
            seq.append(0)
        elif seq_i[i] > 0 and seq_q[i] <= 0:
            seq.append(0)
            seq.append(1)
        elif seq_i[i] <= 0 and seq_q[i] > 0:
            seq.append(1)
            seq.append(0)
        else: 
            seq.append(1)
            seq.append(1)
    return seq

def phase_demodulation(y, args):
    '''
    描述：QPSK解调
    参数：调制波形，参数
    返回：0-1序列
    '''
    framerate = args.framerate
    frequency = args.frequency
    volume = args.volume
    start_place = args.start_place
    interval = args.interval

    seq_i = []
    seq_q = []
    one_num = round(framerate * interval)
    i = 0
    while i < len(y):
        if i + one_num > len(y):
            sub_seq = y[i: ]
        else:
            sub_seq = y[i: i + one_num]
        integral_i = get_integral("sin", sub_seq, frequency, framerate, interval, volume)
        integral_q = get_integral("cos", sub_seq, frequency, framerate, interval, volume)
        seq_i.append(integral_i)
        seq_q.append(integral_q)
        i += one_num
    seq = get_original_seq(seq_i, seq_q)
    return seq