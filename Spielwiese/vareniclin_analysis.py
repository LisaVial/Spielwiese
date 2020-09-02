import numpy as np
import h5py
import matplotlib.pyplot as plt
from IPython import embed

file_path = r'D:\Lisa\data\Andrea\AAV6\Andrea_AAV6_kCl_8mM_analysis.h5'

file = h5py.File(file_path, 'r')

raw_signal = file['Data']['Recording_0']['AnalogStream']['Stream_1']['ChannelData'][:]
labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_1']['InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[0] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_1']['InfoChannel']]
indices = list(np.argsort(same_len_labels))
fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_1']['InfoChannel']['Tick'][0]
ts_labels = [ch[2].decode('utf8') for ch in file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp']]
ts_same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in ts_labels]
ts_indices = np.argsort(ts_same_len_labels)
ts_keys = list(file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys())
first_indices = [idx for idx, label in enumerate(labels) if label[1] == '1' and len(label) == 2]

# heatmap = np.empty((16, 16))
# heatmap[:] = np.nan
# heatmap[0][0] = 0
heatmap = []
ts_ids = [info[0] for info in np.asarray(file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp'])[np.argsort(ts_same_len_labels)]]
# embed()
for id in ts_ids:
    key = 'TimeStampEntity_' + str(id)
    try:
        ts_ch = file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]
        print(ts_ch)
        heatmap.append(ts_ch.shape[1])
    except:
        heatmap.append(0)
structured_heatmap = [[]] * 16
for i in range(16):
    for j in range(16):
        if i == 0 or j == 0 or i == 15 or j == 15:
            structured_heatmap[i].append(0)
        elif
embed()

# convention for this analysis: only take the first ten seconds for plots

# first plot: raw trace vs filtered trace in 2 vertical subplots
# embed()
index = indices[120]
print(labels[index])
plot_signal_raw = raw_signal[index][:int(10*fs)]
plot_signal_filter = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][indices[120]][:int(10*fs)]

time_raw = np.arange(0, int(len(plot_signal_raw)/fs), (1/fs))
time_filter = np.arange(0, int(len(plot_signal_filter)/fs), (1/fs))

fig, axs = plt.subplots(2)
axs[0].plot(time_raw, plot_signal_raw, linewidth=2)
axs[1].plot(time_filter, plot_signal_filter, linewidth=1.5, alpha=0.75)
plt.show()

# embed()