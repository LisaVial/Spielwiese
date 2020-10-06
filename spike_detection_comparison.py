import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as spec
import h5py
import functions as funcs
from IPython import embed

# file: 2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.h5
colors =  ['#749800', '#006d7c']
raw_filepath = r'D:\Lisa\data\Daniela_h5\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.h5'
raw_file = h5py.File(raw_filepath, 'r')
sampling_frequency = 1000000/raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
ordered_indices = funcs.get_ordered_indices(raw_file)
raw_file.close()

mcs_filepath = r'D:\spike_detection_comp\2020-10-05T12-10-18Daniela_spikes.h5'
mcs_file = h5py.File(mcs_filepath, 'r')
mcs_unsorted_spiketimes = np.asarray(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'])
mcs_sorted_spiketimes = []
for idx in ordered_indices:
    # embed()
    key = 'TimeStampEntity_' + str(idx)
    if key in list(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys()):
        mcs_sorted_spiketimes.append(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]/
                                     sampling_frequency)


figure = plt.figure(constrained_layout=True)
spec = spec.GridSpec(ncols=3, nrows=1, figure=figure)

ax_1 = figure.add_subplot(spec[0, 0])
for i, spiketimes in enumerate(reversed(mcs_sorted_spiketimes)):
    # embed()
    if i % 2 == 0:
        c = colors[0]
    else:
        c = colors[1]
    ax_1.scatter(spiketimes[0], np.ones(len(spiketimes[0])) * (i+1), marker='|', color=c)
    ax_1.spines['right'].set_visible(False)
    ax_1.spines['top'].set_visible(False)
    ax_1.get_xaxis().tick_bottom()
    ax_1.get_yaxis().tick_left()
    ax_1.tick_params(labelsize=10, direction='out')

meae_filepath = r'D:\Lisa\data\Daniela_h5\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.meae'
meae_file = h5py.File(meae_filepath, 'r')
embed()


plt.show()
sc_filepath = r'D:\spike_detection_comp\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.result.hdf5'
sc_file = h5py.File(sc_filepath, 'r')
same_len_keys = []
for key in list(sc_file['spiketimes'].keys()):
    if len(key) == 6:
        current_key = key[:5] + '00' + key[-1:]
        same_len_keys.append(current_key)
    elif len(key) == 7:
        current_key = key[:5] + '0' + key[-2:]
        same_len_keys.append(current_key)
    else:
        same_len_keys.append(key)
indices = list(np.argsort(same_len_keys))
# sc_file['spiketimes']['temp_0']
sc_sorted_spiketimes = []
for idx in indices:
    # embed()
    key = 'TimeStampEntity_' + str(idx)
    if key in list(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys()):
        mcs_sorted_spiketimes.append(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]/
                                     sampling_frequency)


embed()