import h5py
import matplotlib.pyplot as plt
import numpy as np
from IPython import embed


def get_channel_id(label):
    for ch in spiketimes_file['Data']['Recording_0']['SegmentStream']['Stream_0']['InfoSegment']:
        if label == ch[3].decode('utf8'):
            return ch[0]


def get_st_channel_id(label):
    for ch in spiketimes_file['/Data/Recording_0/SegmentStream/Stream_0/InfoSegment']:
        if label == ch[3].decode('utf8'):
            return ch[0]


def get_scaled_channel(label):
    # so far unclear: will this be done once? -> might be difficult regarding memory
    # do this for each single channel while the channel is needed -> function has to be called each time when
    # signal is needed
    id = get_channel_id(label)
    vt = voltage_traces[id]
    conversion_factor = \
        spiketimes_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
    exponent = spiketimes_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6
    # 6 = pV -> uV
    scaled_trace = vt * conversion_factor * np.power(10.0, exponent)
    return scaled_trace


def get_scaled_spiketimes():
    # so far unclear: will this be done once? -> might be difficult regarding memory
    # do this for each single channel while the channel is needed -> function has to be called each time when
    # signal is needed
    exponent = spiketimes_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6
    # 6 = pV -> uV
    scaled_trace = spiketimes * np.power(10.0, exponent)
    return scaled_trace


channel_label_list = ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'R2', 'R3',
                      'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'A2', 'B2', 'C2',
                      'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'A3', 'B3', 'C3', 'D3',
                      'E3', 'F3', 'G3', 'H3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'A4', 'B4', 'C4', 'D4', 'E4',
                      'F4', 'G4', 'H4', 'J4', 'K4', 'L4', 'M4', 'N4', 'O4', 'P4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5',
                      'G5', 'H5', 'J5', 'K5', 'L5', 'M5', 'N5', 'O5', 'P5', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6',
                      'H6', 'J6', 'K6', 'L6', 'M6', 'N6', 'O6', 'P6', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
                      'J7', 'K7', 'L7', 'M7', 'N7', 'O7', 'P7', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'J8',
                      'K8', 'L8', 'M8', 'N8', 'O8', 'P8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'J9', 'K9',
                      'L9', 'M9', 'N9', 'O9', 'P9', 'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'J10',
                      'K10', 'L10', 'M10', 'N10', 'O10', 'P10', 'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11',
                      'J11', 'K11', 'L11', 'M11', 'N11', 'O11', 'P11', 'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12',
                      'H12', 'J12', 'K12', 'L12', 'M12', 'N12', 'O12', 'P12', 'A13', 'B13', 'C13', 'D13', 'E13', 'F13',
                      'G13', 'H13', 'J13', 'K13', 'L13', 'M13', 'N13', 'O13', 'P13', 'A14', 'B14', 'C14', 'D14', 'E14',
                      'F14', 'G14', 'H14', 'J14', 'K14', 'L14', 'M14', 'N14', 'O14', 'P14', 'A15', 'B15', 'C15', 'D15',
                      'E15', 'F15', 'G15', 'H15', 'J15', 'K15', 'L15', 'M15', 'N15', 'O15', 'P15', 'B16', 'C16', 'D16',
                      'E16', 'F16', 'G16', 'H16', 'J16', 'K16', 'L16', 'M16', 'N16', 'O16', 'P16']


spiketimes_filepath = '/home/lisa_ruth/Albina/2021-08-02T17-02-59McsRecording slice 1 ctrl 29.06.h5'
spiketimes_file = h5py.File(spiketimes_filepath, 'r')
voltage_traces = spiketimes_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
fs = 1000000 / spiketimes_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
# embed()

all_spikes = []
for channel_label in sorted(channel_label_list):
    try:
        # scaled_channel_trace = get_scaled_channel(label='C12')

        channel_id = get_st_channel_id(channel_label)

        key = 'SegmentData_ts_' + str(channel_id)
        spiketimes = spiketimes_file['Data']['Recording_0']['SegmentStream']['Stream_0'][key]
        all_spikes.append(np.array(spiketimes)/fs)
    except KeyError:
        continue
    # spiketimes = get_scaled_spiketimes()
# # embed()
# spiketimes_t = []
# spiketimes_amp = []
# for st in spiketimes[0][:]:
#     if st < len(scaled_channel_trace):
#         spiketimes_t.append(st)
#         spiketimes_amp.append(scaled_channel_trace[int(st*fs)])
#
# time = np.arange(0, len(scaled_channel_trace)/fs, 1/fs)
# fig_1 = plt.figure(figsize=(12,9))
# # ax1 = fig_1.add_subplot(111)
# # ax1.plot(time, scaled_channel_trace, color='#006e7d', zorder=1)
# # ax1.scatter(spiketimes_t, spiketimes_amp, marker='o', color='red', zorder=2)
# # plt.savefig('/home/lisa_ruth/Albina/mcs_spiketimes_2021-02-26_Hippocampus_channel_H10')
# # plt.show()

fig_2 = plt.figure(figsize=(12,9))
ax_2 = fig_2.add_subplot(111)
ax_2.eventplot(all_spikes)
plt.savefig('/home/lisa_ruth/Albina/Rasterplot')



