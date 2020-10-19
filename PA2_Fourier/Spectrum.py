import os
import argparse
from utils import *
from DFT import *


def show_spectrum():
    parser = argparse.ArgumentParser(description="Choose model")
    parser.add_argument("--type", type=str, default="sin", help="constant/linear/sin/load/add_zero")
    parser.add_argument("--N", type=int, default=16, help="N=16/64/1024")
    parser.add_argument("--place", type=str, default="res1", help="the dir of wav")
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

    amplitude_np = np.fft.fft(y, n = args.N)
    spectrum_np = np.zeros(args.N)
    for i in range(0, args.N):
        spectrum_np[i] = amplitude_np[i].real ** 2 + amplitude_np[i].imag ** 2
    amplitude_mine, spectrum_mine = DFT(args.N, y)
    plot_comparison(x, y, amplitude_np, spectrum_np, amplitude_mine, spectrum_mine)


show_spectrum()