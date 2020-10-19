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
    spectrum_old = np.zeros(y.shape[0])
    for i in range(y.shape[0]):
        spectrum_old[i] = amplitude_old[i].real ** 2 + amplitude_old[i].imag ** 2

    amplitude_new = np.fft.fft(result)
    spectrum_new = np.zeros(result.shape[0])
    for i in range(result.shape[0]):
        spectrum_new[i] = amplitude_new[i].real ** 2 + amplitude_new[i].imag ** 2

    plot_filter(x, amplitude_old, spectrum_old, amplitude_new, spectrum_new)


show_spectrum()