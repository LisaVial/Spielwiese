import h5py
import numpy as np
import scipy.signal as signal
from scipy.signal import filtfilt, butter
import matplotlib.pyplot as plt
from IPython import embed


def get_channel_ids(file):
    ids = [ch[1] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    labels = [ch[4].decode('utf8') for ch in
              file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
    ordered_indices = list(np.argsort(same_len_labels))
    return np.asarray(ids)[ordered_indices]


# def get_scaled_channel(label):
#     # so far unclear: will this be done once? -> might be difficult regarding memory
#     # do this for each single channel while the channel is needed -> function has to be called each time when
#     # signal is needed
#     id_by_label = get_channel_id(label)
#     vt = voltage_traces[id_by_label]
#     conversion_factor = \
#         file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
#     exponent = file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6
#     # 6 = pV -> uV
#     scaled_trace = vt * conversion_factor * np.power(10.0, exponent)
#     return scaled_trace


def get_channel_labels(pad_with_zero=False):
    column_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R']
    labels = []
    for col, c in enumerate(column_characters):
        for row, n in enumerate(range(1, 17)):
            if c == 'A' and n == 1 or c == 'A' and n == 16 or c == 'R' and n == 1 or c == 'R' and n == 16:
                continue
            number_str = str(n)
            if pad_with_zero and n < 10:
                # e.g. '5' -> 'B05'
                number_str = '0' + number_str
            labels.append(c + number_str)
    return labels


def get_ordered_index(label: str):
    # make sure column character is upper case
    column_character = label[0].upper()
    row_number = label[1:]
    corrected_label = column_character + row_number

    # check if label is padded with zero, e.g. 'R02'
    padded_with_zero = (int(row_number) < 10) and (len(label) == 3)

    # find and return index
    return get_channel_labels(padded_with_zero).index(corrected_label)


def butter_filter(cutoff, fs, mode, order=4):
        nyq = 0.5 * fs
        normal_cutoff = cutoff/nyq
        b, a = butter(order, normal_cutoff, btype=mode, analog=False)
        return b, a


def butter_div_filters(data, cutoff_freq, fs, mode):
        # todo: check if this still works
        # as far as I understood it, all three filter types (low, high, notch) can be applied with these functions
        # and which filter will be applied at the end depends on the chosen mode
        b, a = butter_filter(cutoff_freq, fs, mode)
        y = filtfilt(b, a, data)
        return y


filepath = '/home/lisa_ruth/Nikolas/2021-07-12T14-22-24Slice4_0.5Mg2+_504AP_10mMNMDAPuffing_5psi_400ms_2pulses_3sgap.h5'
file = h5py.File(filepath, 'r')

wanted_indices = np.array(['14', '30', '46', '62', '78', '94', '110', '126', '142', '0', '15', '31', '47', '63', '79',
                           '95', '111', '127', '143', '1', '16', '32', '48', '64', '80', '96', '112', '128', '144', '2',
                           '17', '33', '49', '65', '81', '97', '113', '129', '145'], dtype='int32')

ordered_indices = get_channel_ids(file)
print('ordered indices: \n', ordered_indices)

all_channels = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
selected_channels = [all_channels[idx] for idx in ordered_indices[wanted_indices]]
print('selected channels: \n', ordered_indices[wanted_indices])
sampling_frequency = 1000000 / \
                             file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]
labels = get_channel_labels()
wanted_labels = [labels[j] for j in wanted_indices]
print(wanted_labels)

for idx, channel in enumerate(selected_channels):
    print('channel', idx+1, 'of', len(selected_channels))

    # np.abs(channel)
    filtered_channel = butter_div_filters(channel, 25, sampling_frequency, 'low')
    freqs, t, S_xx = signal.spectrogram(filtered_channel[int(4*sampling_frequency):], sampling_frequency,
                                        nperseg=2**16, noverlap=2*15)
    # freqs, t, S_xx = signal.spectrogram(channel[int(4*sampling_frequency):], sampling_frequency, nperseg=2**16,
    #                                     noverlap=2*15)
    # fig_name = 'Spectrogram_' + str(wanted_labels[idx]) + '_wo_filter.png'
    # fig = plt.figure(figsize=(12, 9))
    # ax = fig.add_subplot(111)
    # im = ax.pcolormesh(t, freqs, S_xx, shading='nearest')
    # ax.set_ylim(0, 25)
    # ax.set_ylabel('frequency [Hz]')
    # ax.set_xlabel('time [sec]')
    # cbar = fig.colorbar(im, ax=ax)
    # plt.savefig('/home/lisa_ruth/Nikolas/' + fig_name)
    # embed()
    power_sum = [np.sum(S_xx[freqs <= 25][i]) for i in range(S_xx.shape[1])]
    fig_2 = plt.figure(figsize=(12, 9))
    f2_name = 'power_sum_over_time' + str(wanted_labels[idx]) + '_wo_filter.png'
    ax_2 = plt.subplot(111)
    ax_2.plot(t, power_sum)
    ax_2.set_ylabel('sum of power of freqs under 25 Hz')
    ax_2.set_xlabel('time [sec]')
    plt.savefig('/home/lisa_ruth/Nikolas/' + f2_name)