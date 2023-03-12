from unused_scripts.helper_method import *


def get_mean_adjusted_threshold(buffer, t):
    mu = np.mean(buffer)
    return mu * t


def peak_detection(x, threshold=0.05, width=15):
    x_filt = apply_filter(x - np.mean(x), w_tetha)
    # if np.max(np.abs(x)) != 0:
    #     x = x / np.max(np.abs(x))
    # x_norm = (x - np.mean(x)) / np.std(x)
    y = np.diff(x_filt ** 2)
    # y = y / np.max(y)
    is_high = y > threshold
    print(np.max(y))
    return np.any(is_high)


def rms(x):
    return np.sqrt(np.mean(x ** 2))


def peak_detection_sigma(x):
    y = np.abs(x)
    mu = np.mean(y)
    sigma = np.std(y)
    threshold = mu + 2.5 * sigma
    return np.any(y > threshold)


def base_level(x):
    return np.mean(x)
