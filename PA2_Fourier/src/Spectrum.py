import os
import argparse
import numpy as np
from utils import *
from DFT import *


def show_spectrum():
    parser = argparse.ArgumentParser(description="Choose what you want to do with Fourier")
    parser.add_argument("--type", type=str, default="sin", help="constant/linear/sin/load/add_zero/stft")
    parser.add_argument("--N", type=int, default=16, help="N=16/64/1024")
    parser.add_argument("--place", type=str, default="res1", help="the dir of wav")
    parser.add_argument("--window", type=int, default=16, help="window=16/64/256/1024")
    args = parser.parse_args()
    real_dir = os.path.join('res', args.place + '.wav')

    if args.type == 'constant':
        x, y = constant_wave(args.N)
    elif args.type == 'linear':
        x, y = linear_wave(args.N)
    elif args.type == 'sin':
        x, y = sine_wave(args.N)    
    elif args.type == 'load':
        x, y = load_wave(real_dir)
    elif args.type == 'add_zero':
        old_x, old_y = load_wave(real_dir)
        x, y = add_zero(old_x, old_y)
    elif args.type == 'stft':
        x, y = load_wave(real_dir)
        STFT(y, args.window)
        return
    else: 
        return

    amplitude_np = np.fft.fft(y)
    amplitude_mine = DFT(y)
    plot_comparison(x, y, amplitude_np, amplitude_mine)

if __name__ == "__main__":
    show_spectrum()