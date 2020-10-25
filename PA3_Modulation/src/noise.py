import numpy as np
import matplotlib.pyplot as plt

def get_noise(signal, SNR):
    '''
    描述：生成高斯噪声
    参数：信号本身，信噪比SNR
    返回：噪声
    '''
    signal_mean = signal.mean()
    signal_std = np.sqrt(np.linalg.norm(signal - signal_mean) ** 2 / signal.shape[0])
    noise_mean = signal_mean
    noise_std = signal_std / np.power(10, (SNR / 20))
    noise = np.random.randn(signal.shape[0]) * noise_std + noise_mean
    return noise

def plot_phase(signal, SNR1, SNR2, SNR3):
    '''
    描述：绘制原信号和带高斯噪声的信号
    参数：信号本身，三个信噪比
    返回：无
    '''
    noise1 = get_noise(signal, SNR1)
    noise2 = get_noise(signal, SNR2)
    noise3 = get_noise(signal, SNR3)
    n_frames = signal.shape[0]


    plt.suptitle("Plot wave with and without noises")
    plt.subplots_adjust(hspace = 0.6, wspace = 0.6)
    plt.subplot(2, 2, 1)
    plt.plot(signal, 'blue')
    plt.title("The wave without noise")

    plt.subplot(2, 2, 2)
    plt.plot(signal + noise1)
    plt.title("The wave with Gaussian noise, SNR = {}dB".format(SNR1))

    plt.subplot(2, 2, 3)
    plt.plot(signal + noise2)
    plt.title("The wave with Gaussian noise, SNR = {}dB".format(SNR2))

    plt.subplot(2, 2, 4)
    plt.plot(signal + noise3)
    plt.title("The wave with Gaussian noise, SNR = {}dB".format(SNR3))
    plt.show()