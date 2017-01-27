from scipy.signal import butter, filtfilt


def butter_lowpass(cutoff_freq, sample_freq, order=5):
    '''
    See http://stackoverflow.com/a/25192640/3838691
    '''
    nyq = 0.5 * sample_freq
    normal_cutoff = cutoff_freq / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff_freq, sample_freq, order=5):
    '''
    See http://stackoverflow.com/a/25192640/3838691
    and http://stackoverflow.com/a/13740532/3838691
    '''
    b, a = butter_lowpass(cutoff_freq, sample_freq, order=order)
    y = filtfilt(b, a, data)
    return y
