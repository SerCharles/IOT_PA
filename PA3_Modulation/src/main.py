import random
import argparse
from pulse import pulse_modulation, pulse_demodulation
from utils import save_wave, load_wave

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose the parameters")
    parser.add_argument("--framerate", type = int, default = 48000)
    parser.add_argument("--frequency", type = int, default = 20000)
    parser.add_argument("--sample_width", type = int, default = 2)
    parser.add_argument("--nchannels", type = int, default = 1)
    parser.add_argument("--volume", type = float, default = 1000.0)
    parser.add_argument("--start_place", type = int, default = 0)
    parser.add_argument("--pulse_length", type = float, default = 0.01)
    parser.add_argument("--interval_0", type = float, default = 0.01)
    parser.add_argument("--interval_1", type = float, default = 0.02)
    parser.add_argument("--save_base", type = str, default = 'sound')
    parser.add_argument("--file_name", type = str, default = 'pulse.wav')
    args = parser.parse_args()

    original_seq = []
    for i in range(100):
        num = round(random.random())
        original_seq.append(num)
    print("The original seq is:\n", original_seq)
    save_dir = "pulse.wav"
    the_wave = pulse_modulation(original_seq, args)
    save_wave(the_wave, framerate = args.framerate, sample_width = args.sample_width, nchannels = args.nchannels, save_base = args.save_base, file_name = args.file_name)
    get_wave = load_wave(save_base = args.save_base, file_name = args.file_name)
    get_seq = pulse_demodulation(get_wave, args)
    print("The loaded seq is:\n", get_seq)

    result = compare_seqs(original_seq, get_seq)
    if result:
        print("The original seq and the seq I get is identical, right!")
    else: 
        print("The original seq and the seq I get is not identical, wrong!")


