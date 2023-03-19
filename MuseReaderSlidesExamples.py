import sys
import time
import numpy as np  # Module that simplifies computations on matrices
import matplotlib.pyplot as plt  # Module used for plotting
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import utils  # Our own utility functions
import pandas as pd
from MuseStreamReader import MuseStreamReader


class Band:
    Delta = 0
    Theta = 1
    Alpha = 2
    Beta = 3


def band_split_example():
    """ 1. CONNECT TO EEG STREAM """

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


    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="EEG")
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



def reading_eeg_buffer_data_example():
    # Length of the EEG data buffer (in seconds)
    # This buffer will hold last n seconds of data and be used for calculations
    BUFFER_LENGTH = 5

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = 0.2

    # Index of the channel(s) (electrodes) to be used
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    INDEX_CHANNEL = [1]

    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="EEG")
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


def acc_detection_example():
    BUFFER_LENGTH = 5

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = 0.2

    # Index of the channel(s) (electrodes) to be used
    # 0 = X, 1 = Y, 2 = Z
    INDEX_CHANNEL = [0]

    muse_stream_reader = MuseStreamReader(BUFFER_LENGTH, SHIFT_LENGTH, INDEX_CHANNEL, stream_type="Accelerometer")
    fs = muse_stream_reader.start_stream()
    print(fs)
    try:
        # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
        while True:
            """ 3.1 ACQUIRE DATA """


            # Obtain EEG data from the LSL stream
            eeg_buffer = muse_stream_reader.get_stream_data()
            df = pd.DataFrame(eeg_buffer)
            df.columns = ["X"]

            print(df.head(6))

    except KeyboardInterrupt:
        print('Closing!')


if __name__ == '__main__':
    acc_detection_example()
