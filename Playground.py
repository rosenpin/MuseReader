import numpy as np

from signal_processing import *

fs = 52
data = load_array_from_csv("Accelerometer_recording_2023-03-19-21.08.00.csv")

data = data[1:, 1:]

x = data[:, 0]

x = x / max(abs(x))
w_shake = design_band_filter(fs, 1, 5)

x_smooth = apply_fir_filter(x, np.ones(5) / 5)  # running average of length 5

w_twirl = firwin(31, 0.6, pass_zero=True, fs=fs)

x_shake = apply_fir_filter(x, w_shake)

x_twirl = apply_fir_filter(x, x_smooth)