import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, firwin
from utils import update_buffer
"""
reading / writing functions
"""


def load_array_from_csv(file_path):
    return np.genfromtxt(file_path, delimiter=',')


"""
Plotting functions
"""


def plot_line(x):
    plt.figure()
    plt.plot(x)
    plt.show()


def plot_spectrogram(x, fs):
    plt.figure()
    plt.specgram(x, Fs=fs)


"""
signal processing methods
"""


def apply_fir_filter(x, w):
    return lfilter(w, 1.0, x)


def design_band_filter(fs, fmin, fmax, numtaps=31, is_band_pass=False):
    cutoff = [fmin, fmax]
    w = firwin(numtaps=numtaps, cutoff=cutoff, pass_zero=is_band_pass, fs=fs)
    return w


def notch_filter(x, buffer_length):
    buffer = np.zeros(buffer_length)
    for i in range(len(x) // buffer_length):
        new_data = x[max(i*buffer_length, 0):min((i+1)*buffer_length, len(x))]
        update_buffer()