import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as spec
import h5py
import functions as funcs
from IPython import embed
import spykingcircus as sc

# file: 2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.h5
colors = ['#749800', '#006d7c']
raw_filepath = r'G:\Lisa\data\Daniela_h5\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.h5'
raw_file = h5py.File(raw_filepath, 'r')
sampling_frequency = 1000000/raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
labels = [ch[4].decode('utf8') for ch in raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
ordered_indices = funcs.get_ordered_indices(raw_file)
raw_file.close()

mcs_filepath = r'G:\spike_detection_comp\2020-10-05T12-10-18Daniela_spikes.h5'
mcs_file = h5py.File(mcs_filepath, 'r')
mcs_unsorted_spiketimes = np.asarray(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'])
mcs_sorted_spiketimes = []
for idx in ordered_indices:
    # embed()
    key = 'TimeStampEntity_' + str(idx)
    if key in list(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys()):
        mcs_sorted_spiketimes.append(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]/
                                     sampling_frequency)


figure = plt.figure(figsize=(15, 12), constrained_layout=True)
spec = spec.GridSpec(ncols=3, nrows=1, figure=figure)

ax_1 = figure.add_subplot(spec[0, 0])
for i, spiketimes in enumerate(reversed(mcs_sorted_spiketimes)):
    # embed()
    if i % 2 == 0:
        c = colors[0]
    else:
        c = colors[1]
    ax_1.scatter(spiketimes[0], np.ones(len(spiketimes[0])) * (i+1), marker='|', color=c)
    ax_1.set_title('Multi Channel Systems spike detection')
    ax_1.spines['right'].set_visible(False)
    ax_1.spines['top'].set_visible(False)
    ax_1.get_xaxis().tick_bottom()
    ax_1.get_yaxis().tick_left()
    ax_1.tick_params(labelsize=10, direction='out')
yticklabels = np.asarray(labels)[ordered_indices]
yticklabels = yticklabels[::-1]

ytick_range = np.arange(0, len(mcs_sorted_spiketimes), (int(len(mcs_sorted_spiketimes)/4)))
ax_1.set_yticks(ytick_range)

labels = [item.get_text() for item in ax_1.get_yticklabels()]
empty_string_labels = []
for idx in range(len(yticklabels)):
    if idx % 62 == 0:
        empty_string_labels.append(yticklabels[idx])
ax_1.set_yticklabels(empty_string_labels)
ax_1.set_xticklabels([])
ax_1.set_ylabel('MEA channels')

meae_filepath = \
    r'G:\Lisa\data\data\Daniela GS967\MEA\200506\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.meae'
meae_file = h5py.File(meae_filepath, 'r')

same_len_meae_keys = []
for key in meae_file.keys():
    if 'spiketimes' in key:
        if len(key) == 12:
            current_key = key[:5] + '00' + key[-1:]
            same_len_meae_keys.append(current_key)
        elif len(key) == 13:
            current_key = key[:5] + '0' + key[-2:]
            same_len_meae_keys.append(current_key)
        else:
            same_len_meae_keys.append(key)

meae_indices = list(np.argsort(same_len_meae_keys))

meae_sorted_spiketimes = []
for idx in meae_indices:
    # embed()
    key = 'spiketimes_' + str(idx)
    if key in list(meae_file.keys()):
        # embed()
        meae_sorted_spiketimes.append(meae_file[key][:])
ax_2 = figure.add_subplot(spec[0, 1])

for i, meae_spiketimes in enumerate(reversed(meae_sorted_spiketimes)):
    # embed()
    if i % 2 == 0:
        c = colors[0]
    else:
        c = colors[1]
    ax_2.scatter(meae_spiketimes, np.ones(len(meae_spiketimes)) * (i+1), marker='|', color=c)
    ax_2.set_title('MEAsure spike detection')
    ax_2.spines['right'].set_visible(False)
    ax_2.spines['top'].set_visible(False)
    ax_2.get_xaxis().tick_bottom()
    ax_2.get_yaxis().tick_left()
    ax_2.tick_params(labelsize=10, direction='out')
ax_2.set_yticklabels([])
ax_2.set_xlabel('time [s]')


sc_filepath = r'G:\spike_detection_comp\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.clusters.hdf5'
sc_file = h5py.File(sc_filepath, 'r')
# embed()
same_len_keys = []
for key in list(sc_file.keys()):
    if 'times' in key:
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
    key = 'times_' + str(idx)
    if key in list(sc_file.keys()):
        sc_sorted_spiketimes.append(sc_file[key][:]/
                                     sampling_frequency)

ax_3 = figure.add_subplot(spec[0, 2])
for i, sc_spiketimes in enumerate(reversed(sc_sorted_spiketimes)):
    # embed()
    if i % 2 == 0:
        c = colors[0]
    else:
        c = colors[1]
    ax_3.scatter(sc_spiketimes, np.ones(len(sc_spiketimes)) * (i+1), marker='|', color=c)
    ax_3.set_title('spyKING CIRCUS spike detection')
    ax_3.spines['right'].set_visible(False)
    ax_3.spines['top'].set_visible(False)
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax_3.tick_params(labelsize=10, direction='out')
ax_3.set_yticklabels([])
ax_3.set_xticklabels([])
manager = plt.get_current_fig_manager()
manager.window.showMaximized()
# embed()
plt.savefig('spike_detection_comparison.png')
# plt.savefig('spike_detection_comparison.pdf')
plt.show()



