import h5py
import glob
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


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


folder = '/home/lisa_ruth/spyking-circus/'
files = glob.glob(folder+'*/*Slice4.clusters.hdf5')
bl_file = h5py.File('/home/lisa_ruth/Lisa/human/2021-06-22T16-11-39human_slices_Slice1_Vareniclin_washin.h5', 'r')
active_channels = []
spikecounts = []
# sampling_frequency = 1000000 / \
#                          bl_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
# duration_index = bl_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelDataTimeStamps'][0][2]
# duration_bl = 600
duration = 900
# print(duration_index/sampling_frequency)
for file in sorted(files):
    current_file = h5py.File(file, 'r')
    sts = retrieve_spiketimes(current_file)
    spike_lens = [len(sts[i]) for i in range(len(sts))]
    #
    # if 'BL' in file:
    #     corrected_spike_lens = np.array([spike_lens[j] if spike_lens[j] / duration_bl >= 0.05 else 0
    #                                      for j in range(len(spike_lens))])
    #
    # else:
    corrected_spike_lens = np.array([spike_lens[j] if spike_lens[j] / duration >= 0.05 else 0
                                     for j in range(len(spike_lens))])
    spikecounts.append(np.mean(corrected_spike_lens))
    active_channels.append(len(corrected_spike_lens[corrected_spike_lens > 0]))

print(sorted(files))
print( active_channels)
fig, ax = plt.subplots(1, 1, figsize=(12, 9))
ax.plot(active_channels, 'o--')
ax.set_xticks(range(len(active_channels)))
# ax.set_xticklabels([r'baseline $32^\circ$C', r'baseline $32^\circ$C with K$^+$', r'$38^\circ$C with K$^+$',
#                     r'$\sim 40^\circ$C with K$^+$'])
# ax.set_xticklabels(['potassium \n washin', 'Vareniclin \n washin wo K', 'Vareniclin \n washin high K'])
ax.set_xticklabels(['normal aCSF', 'high K aCSF', 'low Mg and 4AP', 'aCSF with \n high K and \n low Mg and 4AP'])
# ax.set_xticklabels(['baseline', 'Vareniclin \n washin', 'Vareniclin \n washin \n after 30 min', 'Vareniclin \n washout',
#                     'Vareniclin \n washout \n after 1 h'])

ax.set_ylabel('number of active channels')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.savefig('/home/lisa_ruth/lab_seminar/human_acute_spike_counts.png')
print(active_channels)


