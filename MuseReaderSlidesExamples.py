# Python prebuilt packages
import sys
import time

# External Packages imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyautogui

# This Package imports
from src.muselslSource import utils
from src.MuseStreamReader import MuseStreamReader
from src.GestureHandler import GestureHandler
from src.OnlineTimeSeriesPlotter import OnlineTimeSeriesPlotter

"""
these are minor change to the code included in the muselsl example
@misc{muse-lsl,
  author       = {Alexandre Barachant and
                  Dano Morrison and
                  Hubert Banville and
                  Jason Kowaleski and
                  Uri Shaked and
                  Sylvain Chevallier and
                  Juan Jesús Torre Tresols},
  title        = {muse-lsl},
  month        = may,
  year         = 2019,
  doi          = {10.5281/zenodo.3228861},
  url          = {https://doi.org/10.5281/zenodo.3228861}
}

"""


# Handy little enum to make code more readable

class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


def reading_eeg_raw_buffer_data_example():
    # Length of the EEG data buffer (in seconds)
    # This buffer will hold last n seconds of data and be used for calculations
    BUFFER_LENGTH = 5

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = 0.2

    # Index of the channel(s) (electrodes) to be used
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    INDEX_CHANNEL = [0, 1, 2, 3]

    # initialize a stream reader object. It is in charge of the device readings
    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="EEG")
    # start stream
    fs = muse_stream_reader.start_stream()
    print(fs)

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            """ 3.1 ACQUIRE DATA """

            # Obtain EEG data from the LSL stream
            eeg_buffer = muse_stream_reader.get_stream_data()
            df = pd.DataFrame(eeg_buffer)
            df.columns = [["left ear", "left forehead", "right forehead", "right ear"][i] for i in INDEX_CHANNEL]

            print(df.head(6))
    except KeyboardInterrupt:
        print('Closing!')


def band_split_example():
    """ 1. CONNECT TO EEG STREAM and show readings"""

    # Length of the EEG data buffer (in seconds)
    # This buffer will hold last n seconds of data and be used for calculations
    BUFFER_LENGTH = 5

    # Length of the epochs used to compute the FFT (in seconds)
    EPOCH_LENGTH = 1

    # Amount of overlap between two consecutive epochs (in seconds)
    OVERLAP_LENGTH = 0.8

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

    # Index of the channel(s) (electrodes) to be used
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    INDEX_CHANNEL = [1]

    # this is a gesture threshold for relaxation. feel free to tune as needed
    RELAXATION_TRESHOLD = 2.5

    # initialize a stream reader object. It is in charge of the device readings
    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="EEG")
    # starts the stream
    fs = muse_stream_reader.start_stream()

    """ 2. INITIALIZE BUFFERS """

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    band_buffer = np.zeros((n_win_test, 4))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')

    # this is an online time series plotter. set to hold previous results and compare them to a threshold
    viewer = OnlineTimeSeriesPlotter(100, 0, 4, threshold=RELAXATION_TRESHOLD)
    viewer.init_plot()

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            """ 3.1 ACQUIRE DATA """
            # Obtain EEG data from the LSL stream
            eeg_buffer = muse_stream_reader.get_stream_data()

            """ 3.2 COMPUTE BAND POWERS """
            # Get newest samples from the buffer

            data_epoch = utils.get_last_data(eeg_buffer,
                                             EPOCH_LENGTH * fs)

            # Compute band powers
            band_powers = utils.compute_band_powers(data_epoch, fs)
            band_buffer, _ = utils.update_buffer(band_buffer,
                                                 np.asarray([band_powers]))
            # Compute the average band powers for all epochs in buffer
            # This helps to smooth out noise
            smooth_band_powers = np.mean(band_buffer, axis=0)

            # print('Delta: ', band_powers[Band.Delta], ' Theta: ', band_powers[Band.Theta],
            #       ' Alpha: ', band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta])

            """ 3.3 COMPUTE NEUROFEEDBACK METRICS """
            # These metrics could also be used to drive brain-computer interfaces

            # Alpha Protocol:
            # Simple redout of alpha power, divided by delta waves in order to rule out noise
            alpha_metric = smooth_band_powers[Band.Alpha] / \
                           smooth_band_powers[Band.Delta]
            print('Alpha Relaxation: ', alpha_metric)

            # sends last alpha result to the viewer
            viewer.render(alpha_metric)

            """
            Beyond are commented implementations of Beta and Alpha/Theta protocols, Given By muselsl
            """

            # Beta Protocol:
            # Beta waves have been used as a measure of mental activity and concentration
            # This beta over theta ratio is commonly used as neurofeedback for ADHD
            # beta_metric = smooth_band_powers[Band.Beta] / \
            #     smooth_band_powers[Band.Theta]
            # print('Beta Concentration: ', beta_metric)

            # Alpha/Theta Protocol:
            # This is another popular neurofeedback metric for stress reduction
            # Higher theta over alpha is supposedly associated with reduced anxiety
            # theta_metric = smooth_band_powers[Band.Theta] / \
            #     smooth_band_powers[Band.Alpha]
            # print('Theta Relaxation: ', theta_metric)

    except KeyboardInterrupt:
        print('Closing!')


def acc_detection_example():
    from src.signal_processing import firwin

    BUFFER_LENGTH = 1.5

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = 0.05

    # Index of the channel(s) (axis) to be used
    # 0 = X, 1 = Y, 2 = Z
    INDEX_CHANNEL = [0]

    THRESHOLD_SHAKE = 0.25

    # initialize a stream reader object. It is in charge of the device readings
    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="Accelerometer")
    fs = muse_stream_reader.start_stream()

    print(f"sampling rate: {fs}")

# this method is called on successful gesture recognition
    def call_on_shake():
        print("shake detected", file=sys.stderr)
        with pyautogui.hold("space"):
            time.sleep(0.01)

    # here is a demonstration of a GestureHandler object. It is responsible for comparing results against a threshold,
    # handling whatever follows the recognition, and ensures some delay between successful recognitions
    shake_detected_handler = GestureHandler(THRESHOLD_SHAKE, BUFFER_LENGTH, SHIFT_LENGTH)

    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            """ 3.1 ACQUIRE DATA """

            # Obtain EEG data from the LSL stream
            eeg_buffer = muse_stream_reader.get_stream_data()

            # preprocessing - shift to [-1, 1] range
            x = eeg_buffer / max(abs(eeg_buffer))

            # feature number - a head shake is quite sharp so a derivative is a perfect fit
            x_diff = np.diff(x, axis=0)
            # handle edge case where x is of length 0
            if x_diff.size > 0:
                x_diff_peak = max(abs(x_diff))
            else:
                x_diff_peak = 0

            print(x_diff_peak)

            # here we send the model result and the output function to the gesture handler
            shake_detected_handler.evaluate_gesture(x_diff_peak, call_on_shake)

    except KeyboardInterrupt:
        print('Closing!')


if __name__ == '__main__':
    # run this example
    acc_detection_example()
