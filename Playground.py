from signal_processing import *

fs = 52
data = load_array_from_csv("Accelerometer_recording_2023-03-19-21.08.00.csv")

data = data[1:, 1:]

x = data[:, 0]

w_shake = design_band_filter(fs, 1, 3)

x_shake = apply_fir_filter(x, w_shake)