import numpy as np  # Module that simplifies computations on matrices
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data

import utils  # Utility functions from Muselsl
from helper_methods import is_iterable, get_possible_indexes   # More utility functions

# BUFFER_LENGTH = 5
#
# # Length of the epochs used to compute the FFT (in seconds)
# EPOCH_LENGTH = 1
#
# # Amount of overlap between two consecutive epochs (in seconds)
# OVERLAP_LENGTH = 0.8


class MuseStreamReader:

    class StreamError(Exception):
        pass

    def __init__(self, buffer_length_seconds=5, shift_length=0.2, index_channel=None, stream_type="EEG"):
        self.fs = None
        self.inlet = None
        self.buffer_length = buffer_length_seconds
        self.shift_length = shift_length
        self.eeg_buffer = None
        self.filter_state = None
        self.stream_type = stream_type

        # check if index_channel is iterable
        if not is_iterable(index_channel):
            index_channel = [0]
        # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
        self.channels = []
        possible_indexes = get_possible_indexes(stream_type)
        for i in possible_indexes:
            if i in index_channel:
                self.channels.append(i)

    def start_stream(self):
        # Search for active LSL streams
        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', self.stream_type, timeout=2)
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')

        # Set active EEG stream to inlet and apply time correction
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_chunklen=12)
        eeg_time_correction = inlet.time_correction()

        # Get the stream info and description
        info = inlet.info()
        description = info.desc()

        # Get the sampling frequency
        # This is an important value that represents how many EEG data points are
        # collected in a second. This influences our frequency band calculation.
        # for the Muse 2016, this should always be 256
        self.fs = int(info.nominal_srate())
        self.inlet = inlet

        self.eeg_buffer = np.zeros((int(self.fs * self.buffer_length), len(self.channels)))
        return self.fs

    def get_stream_data(self):
        eeg_data, timestamp = self.inlet.pull_chunk(
            timeout=1, max_samples=int(self.shift_length * self.fs))
        # Only keep the channel we're interested in
        ch_data = np.array(eeg_data)[:, self.channels]
        # Update EEG buffer with the new data
        self.eeg_buffer, self.filter_state = utils.update_buffer(
            self.eeg_buffer, ch_data, notch=True,
            filter_state=self.filter_state)
        if len(self.eeg_buffer.shape) != 2:  # this means the stream has failed
            raise MuseStreamReader.StreamError

        return self.eeg_buffer

