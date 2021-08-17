import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as spec
import h5py
from IPython import embed


def get_channel_id(label, file):
    for ch in raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if label == ch[4].decode('utf8'):
            return ch[0]

# file: 2020-10-13T14-27-38FHM3_GS967_BL6_P15_male_400ms_7psi_Slice3_Test1_WITH.h5


raw_filepath = '/home/lisa_ruth/mea_recordings/Daniela_h5/MEA_210217/' \
               '2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1.h5'
raw_file = h5py.File(raw_filepath, 'r')
sampling_frequency = 1000000/raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
id_1 = get_channel_id('A5', raw_file)
id_2 = get_channel_id('C5', raw_file)
id_3 = get_channel_id('F6', raw_file)
ids = [id_1, id_2, id_3]
conversion_factor = raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
exponent = raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6  # 6 = pV -> uV
fig_c = plt.figure(figsize=(9, 6))
ax_c = plt.subplot(111)
for axis in ['top', 'bottom', 'left', 'right']:
  ax_c.spines[axis].set_linewidth(2)

vt_c = raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:][ids[2]]
time = np.arange(0, len(vt_c)/int(sampling_frequency), 1/sampling_frequency)
# time = np.arange(10, 70, 1/sampling_frequency)
scaled_c = vt_c * conversion_factor * np.power(10.0, exponent)
# ax_c.plot(time, scaled_c, color='#006d7c', zorder=1)
ax_c.plot(time, scaled_c, color='#006d7c', zorder=1, linewidth=2.)
ax_c.spines['right'].set_visible(False)
ax_c.spines['top'].set_visible(False)
ax_c.set_ylabel(r'V [$\mu$V]', fontsize=14)
ax_c.set_xlabel('t [s]', fontsize=14)
# ax_c.vlines(10, -60, 60, color='r', linestyle='--', zorder=2, linewidth=2)
# ax_c.vlines(70, -60, 60, color='r', linestyle='--', zorder=2, linewidth=2)
for tick in ax_c.xaxis.get_major_ticks():
    tick.label.set_fontsize(12)
for tick in ax_c.yaxis.get_major_ticks():
    tick.label.set_fontsize(12)
plt.savefig('F6.png')
plt.show()
raw_file.close()
#
# mcs_filepath = '/home/lisa_ruth/mea_recordings/CSD_data/h5_data/' \
#                'Daniela_spikes_presentation.h5'
# mcs_file = h5py.File(mcs_filepath, 'r')
# mcs_unsorted_spiketimes = np.asarray(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'])
# mcs_sorted_spiketimes = []
# for idx in ids:
#     key = 'TimeStampEntity_' + str(idx)
#     if key in list(mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'].keys()):
#         spike_indices = mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0'][key][:]
#         exp = mcs_file['Data']['Recording_0']['TimeStampStream']['Stream_0']['InfoTimeStamp']['Exponent'][0]
#         spiketimes = spike_indices * np.power(10.0, exp)
#         # print(spiketimes[(10 <= spiketimes) & (spiketimes <= 70)])
#         mcs_sorted_spiketimes.append(spiketimes[(10 <= spiketimes) & (spiketimes <= 70)])
#
#
# figure_mcs = plt.figure(figsize=(9, 6), constrained_layout=True)
# # spec = spec.GridSpec(ncols=3, nrows=1, figure=figure)
# yticklabels = ['C9', 'D5', 'M4']
# ax_1 = figure_mcs.add_subplot(111)
# for axis in ['top', 'bottom', 'left', 'right']:
#   ax_1.spines[axis].set_linewidth(2)
# for i, spiketimes in enumerate(reversed(mcs_sorted_spiketimes)):
#     ax_1.scatter(spiketimes, np.ones(len(spiketimes)) * i, marker='|', color='black', linewidth=2)
#     ax_1.set_yticks(range(len(mcs_sorted_spiketimes)))
#     ax_1.set_yticklabels(yticklabels)
#     ax_1.spines['right'].set_visible(False)
#     ax_1.spines['top'].set_visible(False)
#     ax_1.set_ylabel('MEA channel', fontsize=14)
#     ax_1.set_xlabel('time [s]', fontsize=14)
#     ax_1.tick_params(labelsize=14, direction='out')
#     for tick in ax_1.xaxis.get_major_ticks():
#         tick.label.set_fontsize(12)
#     for tick in ax_1.yaxis.get_major_ticks():
#         tick.label.set_fontsize(12)
# ax_1.set_yticklabels(yticklabels)
# ax_1.set_ylabel('MEA channels')
# plt.savefig('MCS_spikes.png')
# plt.show()
#
# meae_filepath = '/home/lisa_ruth/mea_recordings/CSD_data/h5_data/spiketimes.meae'
# meae_file = h5py.File(meae_filepath, 'r')
# # embed()
# meae_sorted_spiketimes = []
# for idx in range(3):
#     # embed()
#     key = 'spiketimes_' + str(idx)
#     if key in list(meae_file.keys()):
#         mea_spikes = meae_file[key][:]
#         meae_sorted_spiketimes.append(mea_spikes[(10 <= mea_spikes) & (mea_spikes <= 70)])
#         print(meae_file[key][:])
#
# figure_meae = plt.figure(figsize=(9, 6), constrained_layout=True)
# ax_2 = figure_meae.add_subplot(111)
# for axis in ['top', 'bottom', 'left', 'right']:
#   ax_2.spines[axis].set_linewidth(2)
# for i, meae_spiketimes in enumerate(reversed(meae_sorted_spiketimes)):
#     # embed()
#     ax_2.scatter(meae_spiketimes, np.ones(len(meae_spiketimes)) * (i+1), marker='|', color='black', linewidth=2)
#     ax_2.spines['right'].set_visible(False)
#     ax_2.spines['top'].set_visible(False)
#     ax_2.get_xaxis().tick_bottom()
#     ax_2.get_yaxis().tick_left()
#     ax_2.tick_params(labelsize=14, direction='out')
#     y_tick_range = range(len(meae_sorted_spiketimes))
#     y_ticks = [y_tick + 1 for y_tick in y_tick_range]
#     ax_2.set_yticks(y_ticks)
#     ax_2.set_yticklabels(yticklabels)
#     ax_2.set_ylabel('MEA channel', fontsize=14)
#     ax_2.set_xlabel('time [s]', fontsize=14)
#     for tick in ax_1.xaxis.get_major_ticks():
#         tick.label.set_fontsize(12)
#     for tick in ax_1.yaxis.get_major_ticks():
#         tick.label.set_fontsize(12)
# plt.savefig('meae_spikes.png')
# plt.show()

sc_filepath = '/home/lisa_ruth/spyking-circus/2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1/'\
              '2021-02-17T15-15-06FHM3_GS967_BL6_P16_female_400ms_7psi_Slice4_Test1.result.hdf5'
sc_file = h5py.File(sc_filepath, 'r')
sc_channel_indices = [166, 234, 180]
sc_sorted_spiketimes = []
for idx in sc_channel_indices:
    key = 'temp_' + str(idx)
    if key in list(sc_file['/spiketimes/'].keys()):
        sc_spikes = sc_file['/spiketimes/'][key][:]/sampling_frequency
        sc_sorted_spiketimes.append(sc_spikes)
        print(sc_spikes[(10 <= sc_spikes) & (sc_spikes <= 70)])

# # embed()
figure_sc = plt.figure(figsize=(9, 6), constrained_layout=True)
ax_3 = figure_sc.add_subplot(111)
for axis in ['top', 'bottom', 'left', 'right']:
  ax_3.spines[axis].set_linewidth(2)
for i, sc_spiketimes in enumerate(reversed(sc_sorted_spiketimes)):
    ax_3.scatter(sc_spiketimes, np.ones(len(sc_spiketimes)) * (i+1), marker='|', color='black', linewidth=2)
    ax_3.set_title('spyKING CIRCUS spike detection')
    ax_3.spines['right'].set_visible(False)
    ax_3.spines['top'].set_visible(False)
    ax_3.get_xaxis().tick_bottom()
    ax_3.get_yaxis().tick_left()
    ax_3.tick_params(labelsize=14, direction='out')
    y_tick_range = range(len(sc_sorted_spiketimes))
    y_ticks = [y_tick + 1 for y_tick in y_tick_range]
    ax_3.set_yticks(y_ticks)
    # ax_3.set_yticklabels(yticklabels)
    ax_3.set_ylabel('MEA channel', fontsize=14)
    ax_3.set_xlabel('time [s]', fontsize=14)
    for tick in ax_3.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
    for tick in ax_3.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
plt.savefig('sc_spikes_threshold_of_6.png')
# plt.savefig('spike_detection_comparison.pdf')
plt.show()



