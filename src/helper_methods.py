import matplotlib.pyplot as plt


class StreamTypes:
    EEG = "EEG"
    ACC = "Accelerometer"
    GYRO = "Gyroscope"
    PPG = "PPG"


def is_iterable(x):
    """
    returns true iff x is iterable
    """
    try:
        _ = iter(x)
        return True
    except TypeError:
        return False


def get_possible_indexes(reading_type="EEG"):
    """
    EEG readings has four channels. Others have three
    """
    if reading_type == "EEG":
        return list(range(4))
    else:
        return list(range(3))


