import numpy as np
import h5py
import matplotlib.pyplot as plt
import matplotlib.gridspec as spec
from matplotlib.colors import LogNorm
import seaborn as sns
# from thunderfish import eventdetection
from IPython import embed


# file_path = r'D:\Lisa\data\Andrea\AAV6\Andrea_AAV6_kCl_8mM_analysis.h5'
files = [r'G:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_analysis.h5',
         r'G:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_10nM_Verenicline_analysis.h5',
         r'G:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_10nM_Verenicline_analysis_washout.h5']
# file_path = \
#     r'G:\Lisa\data\Andrea\AAV5\2020-09-03T15-58-552020-06-16T14-15-21AAV5PSAMCamIIGFP KCl9.6mM_analysis.h5'
heatmap = []
for file in files:
    file = h5py.File(file, 'r')
    fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
    # labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    # same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
    # ch_ids = [ch[0] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    # indices = list(np.argsort(same_len_labels))
    # heatmap = []
    # for i, index in enumerate(indices):
    #     signal = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][index]
    #     duration = (file['Data']['Recording_0'].attrs['Duration'] * 10**-6)
    #     window_size = fs
    #     spikes = []
    #     for step in np.arange(0, int(duration * fs), int(window_size)):
    #         snippet = signal[int(step):int(step+window_size)]
    #         threshold = 5*np.std(snippet)
    #         peak_indices, trough_indices = eventdetection.detect_peaks(snippet, threshold)
    #         approved_spiketimes = [(peak_index + step) / fs for peak_index, trough_index in zip(peak_indices, trough_indices)
    #                                if np.abs((trough_index / fs) - (peak_index / fs)) > 0.1
    #                                and snippet[peak_index] - snippet[trough_index] > 500]
    #         # embed()
    #         spikes += approved_spiketimes
    #     heatmap.append(len(spikes))
    #     print('channel ', i, ' from ', len(indices), ' complete.')
    # heatmap.insert(0, 0)
    # heatmap.insert(15, 0)
    # heatmap.insert(15*16, 0)
    # heatmap.insert(-1, 0)
    # heatmap = np.reshape(heatmap, (16, 16))

    ts_labels = [ch[2].decode('utf8') for ch in file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp']]
    ts_same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in ts_labels]
    ts_indices = np.argsort(ts_same_len_labels)
    ts_keys = list(file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys())

    single_heatmap = []
    ts_ids = [info[0] for info in np.asarray(file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp'])[np.argsort(ts_same_len_labels)]]
    for id in ts_ids:
        key = 'TimeStampEntity_' + str(id)
        try:
            ts_ch = file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]
            ts_ch_last_minutes = [ts for ls in ts_ch for ts in ls if ts >= (60*25*fs)]
            single_heatmap.append(len(ts_ch_last_minutes))
            # print(heatmap)
        except:
            single_heatmap.append(0)
    single_heatmap.insert(0, 0)
    single_heatmap.insert(15, 0)
    single_heatmap.insert(15*16, 0)
    single_heatmap.insert(-1, 0)
    single_heatmap = np.reshape(single_heatmap, (16, 16))
    heatmap.append(single_heatmap)

fig = plt.figure(figsize=(12, 6), constrained_layout=True)
spec2 = spec.GridSpec(ncols=3, nrows=1, figure=fig)
ax1 = fig.add_subplot(spec2[0, 0])
ax2 = fig.add_subplot(spec2[0, 1])
ax3 = fig.add_subplot(spec2[0, 2])

log_norm = LogNorm(vmin=0.1, vmax=np.max(heatmap))
# cbar_ticks = [math.pow(10, i) for i in np.arange(0, 1+np.ceil(math.log10(np.max(heatmap))))]

y_labels = range(1, 17)
x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R']
xticks = np.arange(0.5, 16.5, 1)
sns.heatmap(heatmap[0], cmap='PuBuGn', vmin=0.1, vmax=np.max(heatmap), ax=ax1, cbar=False)
yticks = np.arange(0.5, 16.5, 1)
ax1.set_xticks(xticks)
ax1.set_yticks(yticks)
ax1.set_yticklabels(y_labels)
ax1.set_xticklabels(x_labels)
ax1.set_ylabel('MEA rows')
sns.heatmap(heatmap[1], cmap='PuBuGn', ax=ax2, vmin=0.1, vmax=np.max(heatmap), cbar=False)
ax2.set_xticks(xticks)
ax2.set_yticks(yticks)
ax2.set_yticklabels(y_labels)
ax2.set_xticklabels(x_labels)
sns.heatmap(heatmap[1], cmap='PuBuGn', ax=ax3, norm=log_norm, vmin=0.1, vmax=np.max(heatmap),
            cbar_kws={"ticks": [0.1, 1, 10, 1e2, 1e3, 1e4, 1e5]})
ax3.set_xticks(xticks)
ax3.set_yticks(yticks)
ax3.set_yticklabels(y_labels)
ax3.set_xticklabels(x_labels)
plt.savefig('Andrea_AAV5_heatmap_last_seconds_log_cbar.png')
plt.show()