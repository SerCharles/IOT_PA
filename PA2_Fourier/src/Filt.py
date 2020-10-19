import os
import argparse
from utils import *
from DFT import *
from filters import *

def show_spectrum():
    parser = argparse.ArgumentParser(description="Choose what you want to do with Filters")
    parser.add_argument("--type", type=str, default="moving_average", help="moving_average, bandpass")
    parser.add_argument("--place", type=str, default="res1", help="the dir of wav")
    parser.add_argument("--window", type=int, default=3, help="window=3/4/8/16")
    args = parser.parse_args()
    real_dir = os.path.join('res', args.place + '.wav')
    x, y = load_wave(real_dir)

    if args.type == 'moving_average':
        result = moving_average(y, args.window)
    elif args.type == 'bandpass':
        result = bandpass(x, y)

    amplitude_old = np.fft.fft(y)
    amplitude_new = np.fft.fft(result)


    plot_filter(x, amplitude_old, amplitude_new)


show_spectrum()