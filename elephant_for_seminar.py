import elephant.statistics
import neo
import numpy as np
import h5py
import matplotlib.pyplot as plt
from circus.shared.parser import CircusParser
import quantities as pq
from elephant import kernels


def retrieve_spiketimes(file):
    same_len_keys = []
    for key in list(file.keys()):
        if 'times' in key:
            if len(key) == 6:
                current_key = key[:5] + '00' + key[-1:]
                same_len_keys.append(current_key)
            elif len(key) == 7:
                current_key = key[:5] + '0' + key[-2:]
                same_len_keys.append(current_key)
            else:
                same_len_keys.append(key)
    indices = np.argsort(same_len_keys)

    sorted_spiketimes = []
    for idx in indices:
        key = 'times_' + str(idx)
        if key in list(file.keys()):
            sorted_spiketimes.append(file[key][:])
    return sorted_spiketimes


def make_label_spiketimes_map(ordered_labels, spiketimes, dead_channels):
    label_spiketimes_map = dict()

    live_channel_index = 0
    for index, label in enumerate(ordered_labels):
        if index in dead_channels:
            continue

        label_spiketimes_map[label] = spiketimes[live_channel_index]
        live_channel_index += 1

    return label_spiketimes_map


base_filepath = '/home/lisa_ruth/spyking-circus/' \
                '2021-06-22T15-51-27human_slices_Slice1_BL.h5'
filepath = '/home/lisa_ruth/spyking-circus/2021-06-22T15-51-27human_slices_Slice1_BL/' \
           '2021-06-22T15-51-27human_slices_Slice1_BL.clusters.hdf5'

file = h5py.File(filepath, 'r')
basefile = h5py.File(base_filepath, 'r')

sampling_frequency = 1000000 / \
                         basefile['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
duration_index = basefile['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelDataTimeStamps'][0][2]
duration = duration_index/sampling_frequency
print(duration)
params = CircusParser(base_filepath)
dead_channels = params.get('detection', 'dead_channels')
if len(dead_channels) > 1:
    dead_channels = [int(s) for s in dead_channels[5:-2].split(',')]

ids = [ch[0] for ch in basefile['Data/Recording_0/AnalogStream/Stream_0/InfoChannel']]
labels = [ch[4].decode('utf8') for ch in basefile['Data/Recording_0/AnalogStream/Stream_0/InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ordered_indices_for_ids = np.array(np.argsort(same_len_labels))

ordered_labels = np.array(labels)[ordered_indices_for_ids]
print(1/sampling_frequency * pq.s)
sts = retrieve_spiketimes(file)

label_spiketimes_map = make_label_spiketimes_map(ordered_labels, sts, dead_channels)
spiketimes = label_spiketimes_map['L2']/sampling_frequency
spiketimes = spiketimes[spiketimes<=900]
kernel = kernels.GaussianKernel(sigma=1 * pq.s)
# plt.plot(kernel)
# plt.savefig('/home/lisa_ruth/lab_seminar/kernel.png')
# spike_object = neo.SpikeTrain(spiketimes, units='sec', t_stop=900.0)
# sr = elephant.statistics.instantaneous_rate(spike_object, 1/sampling_frequency * pq.s, kernel=kernel)
# figure, ax = plt.subplots(1, 1, figsize=(12, 9))
# ax.plot(np.linspace(0, 900.0, len(sr)), sr)
# print(np.linspace(0, 900.0, len(sr))[:5])
# # ax.set_xlim([0, 60])
# ax.set_xlabel('time [s]')
# ax.set_ylabel('firing rate [Hz]')
# ax.set_yticks(range(0, len(ordered_labels), 16))
# # ax.set_yticklabels(np.flip(ordered_labels)[::16])
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.get_xaxis().tick_bottom()
# ax.get_yaxis().tick_left()
# plt.savefig('/home/lisa_ruth/lab_seminar/human_organotypic_Vareniclin_washout_after1h_L2_sr.png')
figure, ax = plt.subplots(1, 1, figsize=(12, 9))
ax.eventplot(sts/sampling_frequency)
ax.set_xlim([0, 900])
ax.set_xlabel('time [s]')
ax.set_ylabel('MEA channels')
ax.set_yticks(range(0, len(ordered_labels), 16))
ax.set_yticklabels(ordered_labels[::16])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.savefig('/home/lisa_ruth/lab_seminar/human_organotypic_Vareniclin_BL.svg')
#
#
