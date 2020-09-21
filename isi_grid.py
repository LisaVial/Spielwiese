import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import h5py
import seaborn as sns
from IPython import embed

figure = plt.figure(figsize=(12.8, 9.6), frameon=False)
gs = gridspec.GridSpec(16, 16, wspace=None, hspace=None)


filename = r'D:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_analysis.h5'

file = h5py.File(filename, 'r')

fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_1']['InfoChannel']['Tick'][0]
ts_labels = [ch[2].decode('utf8') for ch in file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp']]
ts_same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in ts_labels]
ts_indices = np.argsort(ts_same_len_labels)
ts_keys = list(file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys())
ts_ids = [info[0] for info in np.asarray(file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp'])[np.argsort(ts_same_len_labels)]]

for g in gs:
    ax = plt.subplot(g)

    row = g.rowspan.start
    column = g.colspan.start
    if (row == 0 and column == 0) or (row == 0 and column == 15) or (row == 15 and column == 0) or (row == 15 and
                                                                                                    column ==15):
        ax.plot(0, 0)
        ax.axis('off')
    else:
        id_index = 16*row + column
        # (0,0) is missing
        id_index -= 1
        if row > 0:
            #(0,15) is missing
            id_index -=1
        if row == 15:
            # (15,0) is missing
            id_index -=1

        id = ts_ids[id_index]

        key = 'TimeStampEntity_' + str(id)

        try:
            ts_ch = file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]
            if 500 >= len(ts_ch[0]) > 0:
                spike_times = (ts_ch/fs)
                isis = np.diff(spike_times)
                xvals = range(len(isis[0]))
                ax.bar(xvals, isis[0], width=0.5, align='center')
                ax.set_xlim([0, 501])
                ax.set_xticks([])
                ax.set_xticklabels([])
                ax.set_yticks([])
                ax.set_yticklabels([])
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
            else:
                ax.plot(0, 0)
                ax.set_xticks([])
                ax.set_xticklabels([])
                ax.set_yticks([])
                ax.set_yticklabels([])
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
        except:
            ax.plot(0, 0)
            ax.set_xticks([])
            ax.set_xticklabels([])
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
plt.style.use('seaborn-white')
plt.show()