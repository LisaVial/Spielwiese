import numpy as np
import matplotlib.pyplot as plt
import h5py
import seaborn as sns



filename = r'D:\Lisa\data\Andrea\Andrea_AAV6_kCl_8mM_analysis.h5'

file = h5py.File(filename, 'r')

fs = 1000000/file['Data']['Recording_0']['AnalogStream']['Stream_1']['InfoChannel']['Tick'][0]
ts_labels = [ch[2].decode('utf8') for ch in file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp']]
ts_same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in ts_labels]
ts_indices = np.argsort(ts_same_len_labels)
ts_keys = list(file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys())
ts_ids = [info[0] for info in np.asarray(file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp'])[np.argsort(ts_same_len_labels)]]

for id in ts_ids:
    key = 'TimeStampEntity_' + str(id)
    print(id)
    try:
        ts_ch = file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]
        if len(ts_ch[0]) > 250:
            figure = plt.figure(figsize=(12.8, 9.6), frameon=False)
            ax = plt.subplot(111)
            spike_times = (ts_ch / fs)
            isis = np.diff(spike_times)
            print(isis)
            xvals = range(len(isis[0]))
            ax.bar(xvals, isis[0])
            ax.set_xlabel('# of spike pair')
            ax.set_ylabel('inter spike interval [s]')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            plt.savefig(str(id) + '_example.png')
            plt.show()
    except:
        continue
