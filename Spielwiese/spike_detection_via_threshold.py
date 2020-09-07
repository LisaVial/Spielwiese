import numpy as np
import h5py
import matplotlib.pyplot as plt
from IPython import embed


file_path = r'D:\Lisa\data\Andrea\AAV6\Andrea_AAV6_kCl_8mM_analysis.h5'

file = h5py.File(file_path, 'r')
fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]

labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[0] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
indices = list(np.argsort(same_len_labels))
signals = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
for i, index in enumerate(indices):
    signal = signals[index]
    threshold = 5 * (np.median(np.abs(signal)/0.6745))
    spike_indices = [idx for idx, point in enumerate(signal) if point >= threshold or -point <= -threshold]
    plt.plot(signal, zorder=1)
    plt.hlines(threshold, 0, len(signal))
    plt.scatter(spike_indices, np.ones(len(spike_indices)) * 100, marker='o', color='k', zorder=2)
    plt.show()
