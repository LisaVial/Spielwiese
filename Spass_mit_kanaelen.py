import numpy as np
import matplotlib.pyplot as plt
import h5py


file_path = r'C:\Users\Imaris\Desktop\Lisa\data\Daniela_h5'
file_name = r'\2020-07-30T13-39-29FHM3_GS967_BL6_P17_female_400ms_7psi_Slice5_Test1.h5'
file_name_2 = r'\2020-07-30T16-51-57FHM3_GS967_BL6_P17_female_400ms_7psi_Slice5_Test1.h5'

file2 = h5py.File(file_path+file_name_2, 'r')
#
# # embed()
signal = file2['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
labels = [ch[4].decode('utf8') for ch in file2['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[0] for ch in file2['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
indices = list(np.argsort(same_len_labels))
csd = signal[ch_ids[indices[7]]]
plt.plot(csd[:100000])
plt.show()

# embed()
# plot_signal = signal[ch_ids[indices[0]]]
# noise_std = np.std(plot_signal)
# spike_treshold_2 = -5 * noise_std
#

# file = h5py.File(file_path+file_name, 'r')
# embed()
# voltages = file['filter'][:]
# plt.plot(signal[ch_ids[indices[0]]], zorder=1)
# plt.hlines(spike_treshold_2, 0, len(plot_signal), color='red', zorder=2)
#
# noise_std_f = np.std(voltages[0])
# spike_treshold_f = -5 * noise_std_f
# plt.plot(voltages[0], zorder=1)
# plt.hlines(spike_treshold_f, 0, len(voltages[0]), color='green', zorder=2)
# plt.show()
