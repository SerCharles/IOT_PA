import random
import argparse
from phase import phase_modulation, phase_demodulation
from utils import save_wave, load_wave, fill_seq, compare_seqs, generate_random_seq



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose the parameters")
    parser.add_argument("--framerate", type = int, default = 48000)
    parser.add_argument("--frequency", type = int, default = 20000)
    parser.add_argument("--sample_width", type = int, default = 2)
    parser.add_argument("--nchannels", type = int, default = 1)
    parser.add_argument("--volume", type = float, default = 1.0)
    parser.add_argument("--start_place", type = int, default = 0)
    parser.add_argument("--interval", type = float, default = 0.025)
    parser.add_argument("--save_base", type = str, default = 'sound')
    parser.add_argument("--file_name", type = str, default = 'phase.wav')
    parser.add_argument("--seq_len", type = int, default = 100)
    args = parser.parse_args()

    original_seq = generate_random_seq(args.seq_len)
    original_seq = fill_seq(original_seq)
    print("The original seq is:\n", original_seq)

    the_wave = phase_modulation(original_seq, args)
    save_wave(the_wave, framerate = args.framerate, sample_width = args.sample_width, nchannels = args.nchannels, save_base = args.save_base, file_name = args.file_name)
    get_wave = load_wave(save_base = args.save_base, file_name = args.file_name)
    get_seq = phase_demodulation(get_wave, args)
    print("The loaded seq is:\n", get_seq)

    result = compare_seqs(original_seq, get_seq)
    if result:
        print("The original seq and the seq I get is identical, right!")
    else: 
        print("The original seq and the seq I get is not identical, wrong!")