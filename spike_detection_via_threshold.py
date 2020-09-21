import numpy as np
import h5py
import matplotlib.pyplot as plt
from IPython import embed


def get_spike_indices(signal, threshold):
    indices = []
    above_upper_threshold = False
    below_lower_threshold = False
    current_extreme_index_and_value = None  # current local minimum or maximum
    for index, value in enumerate(signal):

        if above_upper_threshold:  # last value was above positive threshold limit
            if value <= threshold:  # leaving upper area
                # -> add current maximum index to list (unless its empty)
                indices.append(current_extreme_index_and_value[0])
            else:  # still above positive threshold
                # check if value is bigger than current maximum
                if value > current_extreme_index_and_value[1]:
                    current_extreme_index_and_value = (index, value)

        elif below_lower_threshold:  # last value was below negative threshold limit
            if value <= threshold:  # leaving lower area
                # -> add current minimum index to list (unless its empty)
                indices.append(current_extreme_index_and_value[0])
            else:  # still below negative threshold
                    # check if value is smaller than current maximum
                    if value < current_extreme_index_and_value[1]:
                        current_extreme_index_and_value = (index, value)

        else:  # last value was within threshold limits
            if value > threshold or value < -threshold:  # crossing threshold limit
                # initialise new local extreme value
                current_extreme_index_and_value = (index, value)

        # update state
        below_lower_threshold = (value < -threshold)
        above_upper_threshold = (value > threshold)

    return indices


file_path = r'D:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_analysis.h5'

file = h5py.File(file_path, 'r')
fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]

labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[0] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
indices = list(np.argsort(same_len_labels))
signals = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
for i, index in enumerate(indices):
    signal = signals[index]
    threshold = 4 * (np.median(np.abs(signal)/0.6745))
    #spike_indices = [idx for idx, point in enumerate(signal) if point >= threshold or point <= -threshold]
    spike_indices = get_spike_indices(signal, threshold)
    plt.plot(signal, zorder=1)
    plt.hlines(threshold, 0, len(signal))
    #plt.scatter(spike_indices, np.ones(len(spike_indices)) * 100, marker='o', color='k', zorder=2)
    spike_ys = [signal[index] for index in spike_indices]
    plt.scatter(spike_indices, spike_ys, marker='o', color='k', zorder=2)
    plt.show()
