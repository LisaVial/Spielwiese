import McsPy
import McsPy.McsData
from McsPy import ureg, Q_
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz
from IPython import embed
import os

file_path = \
    r'G:\Lisa\data\2020-07-30T16-51-57FHM3_GS967_BL6_P17_female_400ms_7psi_Slice5_Test1_filtered_100_3000Hz_spikes.h5'
file = McsPy.McsData.RawData(file_path)
file_name = os.path.split(file.raw_data_path)[1][:-3]
file_name = file_name.replace(" ", "_")
electrode_stream = file.recordings[0].analog_streams[0]
ids = [c.channel_id for c in electrode_stream.channel_infos.values()]
labels = [electrode_stream.channel_infos[id].info['Label'] for id in ids]
same_len_labels = [str(label[0])+'0'+str(label[1]) if len(label) < 3 else label for label in labels]
y_tick_labels = []
fig = plt.figure(figsize=[9, 6])
ax = fig.add_subplot(111)
# embed()
for idx, ch_id in enumerate(reversed(np.argsort(same_len_labels))):
    if same_len_labels[ch_id] == 'A02' or same_len_labels[ch_id] == 'R02' or '01' in same_len_labels[ch_id]:
        y_tick_labels.append(labels[ch_id])
    else:
        y_tick_labels.append('')
    try:
        timestamps = file.recordings[0].timestamp_streams[0].timestamp_entity[ch_id].get_timestamps()
        if ch_id % 24 == 0:
            signal = electrode_stream.get_channel_in_range(ch_id, 0, 10000)
            plt.plot(signal[0])
            ax_0 = plt.gca()
            ax_0.spines['right'].set_visible(False)
            ax_0.spines['top'].set_visible(False)
            ax_0.set_yticklabels(y_tick_labels)
            plt.show()
        ax.scatter(timestamps[0], np.ones(len(timestamps[0][0])) * idx, marker='|', c=np.arange(len(timestamps[0][0])),
                   cmap="PuBuGn")
    except KeyError:
        continue
print(y_tick_labels)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_yticklabels(y_tick_labels)
ax.set_yticks(range(252))
ax.set_ylabel('MEA channels')
xlims = ax.get_xlim()
ax.set_xticks([0, xlims[1] / 2, xlims[1]])
ax.set_xlim([0, xlims[1]])
ax.set_xticklabels(['0', '150', '300'])
ax.set_xlabel('time [s]')
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(labelsize=10, direction='out')
plt.savefig(file_name+'_rasterplot.png')
plt.savefig(file_name+'_rasterplot.pdf')
plt.show()