import h5py
import numpy as np
import elephant
import quantities as pq
import viziphant
import neo
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from circus.shared.parser import CircusParser
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

mpl.rcParams['agg.path.chunksize'] = 10000

file_path_sc_base = r'/home/lisa_ruth/spyking-circus/' \
                    r'2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1_rdy_4_SC.h5'
file_path_sc_result = r'/home/lisa_ruth/spyking-circus/' \
                      r'2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1_rdy_4_SC/' \
                      r'2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1_rdy_4_SC.clusters.hdf5'

base_file = h5py.File(file_path_sc_base, 'r')
result_file = h5py.File(file_path_sc_result, 'r')

fs = 10000.

bf_vt = base_file['scaled']
time = np.arange(0, len(bf_vt[0])/fs, 1/fs)

params = CircusParser(file_path_sc_base)
embed()
spiketimes = retrieve_spiketimes(result_file)
labels = ['A5', 'A6', 'B5', 'B6']

figure, axs = plt.subplots(2, 2, figsize=(12, 9))
figure.subplots_adjust(hspace=0.5)
axs = axs.flat
neo_spiketrains = []
for i, ax in enumerate(axs):
    spike_indices = spiketimes[i]
    scatter_time = np.array(time[spike_indices])
    neo_spiketrains.append(neo.SpikeTrain(times=scatter_time, units='sec', t_stop=300.0))
    scatter_height = np.array(bf_vt[i][spike_indices])
    ax.plot(time, bf_vt[i], zorder=1)
    ax.scatter(scatter_time, scatter_height, color='r', zorder=2)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title(f'channel {labels[i]}')
    ax.set_xlabel('time [s]')
    ax.set_ylabel(r'voltage [$\mu$V]')
    # ax.set_xlim([10, 12])
plt.savefig('sc_test.png')
plt.show()

viziphant.rasterplot.rasterplot(neo_spiketrains, color='black')
plt.show()

viziphant.statistics.plot_isi_histogram(neo_spiketrains[0], cutoff=300*pq.s, histtype='bar')


# print('finished')




