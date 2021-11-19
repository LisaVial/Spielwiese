import h5py
import numpy as np
import quantities as pq
from scipy.signal import hilbert, savgol_filter, find_peaks
import matplotlib.pyplot as plt
import csv
import os
from IPython import embed


def get_channel_ids(file):
    ids = [ch[1] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    labels = [ch[4].decode('utf8') for ch in
              file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
    ordered_indices = list(np.argsort(same_len_labels))
    return np.asarray(ids)[ordered_indices]


def get_scaled_channel(vt):
    # so far unclear: will this be done once? -> might be difficult regarding memory
    # do this for each single channel while the channel is needed -> function has to be called each time when
    # signal is needed
    conversion_factor = \
        file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
    exponent = file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6
    # 6 = pV -> uV
    scaled_trace = vt * conversion_factor * np.power(10.0, exponent)
    return scaled_trace


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


filepath = \
    r'/mnt/Data/Nikolas/2021-07-12T14-22-24Slice4_0.5Mg2+_504AP_10mMNMDAPuffing_5psi_400ms_2pulses_3sgap.h5'
file = h5py.File(filepath, 'r')

wanted_indices = np.array(['14', '30', '46', '62', '78', '94', '110', '126', '142', '0', '15', '31', '47', '63', '79',
                           '95', '111', '127', '143', '1', '16', '32', '48', '64', '80', '96', '112', '128', '144', '2',
                           '17', '33', '49', '65', '81', '97', '113', '129', '145'], dtype='int32')

ordered_indices = get_channel_ids(file)

all_channels = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
selected_channels = [all_channels[idx] for idx in ordered_indices[wanted_indices]]
sampling_frequency = 1000000 / \
                             file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']['Tick'][0]

labels = get_channel_labels()
wanted_labels = [labels[j] for j in wanted_indices]
duration_index = file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelDataTimeStamps'][0][2]
duration = duration_index * (1 / sampling_frequency)

file_path = '/mnt/Data/Nikolas/0_HT/'
csv_filename = '2021-07-12T14-22-24Slice4_0.5Mg2+_504AP_10mMNMDAPuffing_5psi_400ms_2pulses_3sgap_HT.csv'
with open(os.path.join(file_path, csv_filename), 'w', newline='') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(['label', 'start time', 'end time', 'duration'])

    for idx, channel in enumerate(selected_channels):

        channel = get_scaled_channel(channel)
        t = np.arange(0, len(channel)/sampling_frequency, 1/sampling_frequency) * pq.s
        filtered_channel = savgol_filter(channel, 1001, 4)

        analytic_signal = hilbert(filtered_channel)
        threshold = 2 * np.median(np.absolute(filtered_channel) / 0.6745)
        # threshold = 4 * np.std(filtered_channel)  # threshold according to Rigas et al., 2015

        angles = np.angle(analytic_signal)
        amplitudes = np.abs(analytic_signal)

        binned_time = np.linspace(0, int(np.ceil(duration)), int(np.ceil(duration)))
        binned_values = [np.mean(amplitudes[int(i*sampling_frequency):int((i+1)*sampling_frequency)])
                         for i in binned_time[:-1]]

        min_peaks_per_seizure = 4

        epileptic_indices = []
        # start at the 6th value (because of puffing artefact) and go through the values in bins of ten
        for bin_idx in range(6, len(binned_time[:-6])):
            # print('bin index:', bin_idx)
            middle_bin = binned_values[bin_idx]
            if middle_bin < threshold:
                continue  # skip middle bins below threshold

            neighbours = []

            for ci in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]:
                # print('comparison index:', ci)
                if binned_values[bin_idx+ci] >= threshold:
                    neighbours.append(bin_idx + ci)

            if len(neighbours) >= 3:
                epileptic_indices += [bin_idx] + neighbours

        epileptic_peak_indices = set()
        for epileptic_index in epileptic_indices:
            epileptic_peak_indices.add(epileptic_index)
        epileptic_indices_list = list(epileptic_peak_indices)
        epileptic_indices_list.sort()
        print("Indices for channel " + wanted_labels[idx] + ":", epileptic_indices_list)

        if len(epileptic_indices_list) < min_peaks_per_seizure:
            print("Not enough indices found for channel " + wanted_labels[idx])
            continue

        above_threshold_time = [binned_time[b_idx] for b_idx in epileptic_indices_list]
        above_threshold_values = [binned_values[b_idx] for b_idx in epileptic_indices_list]

        fig_1 = plt.figure(figsize=(12, 9))
        f1_name = os.path.join(file_path, 'HT_bar_with_threshold_crossings_' + str(wanted_labels[idx]) + '.png')
        ax_1 = plt.subplot(111)
        ax_1.bar(binned_time[:-1], binned_values)
        ax_1.bar(above_threshold_time, above_threshold_values, color='r')
        ax_1.axhline(threshold, 0, int(np.ceil(duration)), ls='--')
        ax_1.set_ylabel('mean envelope')
        ax_1.set_xlabel('time [sec]')
        ax_1.spines['right'].set_visible(False)
        ax_1.spines['top'].set_visible(False)
        ax_1.get_xaxis().tick_bottom()
        ax_1.get_yaxis().tick_left()
        plt.savefig(f1_name)
        plt.clf()

        print('For channel', wanted_labels[idx], 'the start time was', binned_time[epileptic_indices_list[0]],
              'and the end time', binned_time[epileptic_indices_list[-1]])
        w.writerow(
            [wanted_labels[idx], binned_time[epileptic_indices_list[0]], binned_time[epileptic_indices_list[-1]],
             binned_time[epileptic_indices_list[-1]] - binned_time[epileptic_indices_list[0]]])

        # fig_2 = plt.figure(figsize=(12, 9))
        # f2_name = 'power_sum_over_time' + str(wanted_labels[idx]) + '_wo_filter.png'
        # ax_2 = plt.subplot(111)
        # # ax_1.plot(t, neo_channel)
        # # ax_1.plot(t, filtered_channel, zorder=1)
        # # ax_1.plot(t, angles)
        # ax_2.plot(t, np.abs(analytic_signal), color='r', zorder=2, linestyle='--', alpha=.5)
        # # ax_1.plot(t, -np.abs(analytic_signal), color='r', zorder=2, linestyle='--', alpha=.5)
        # ax_2.scatter(scatter_time, scatter_amp, color='black', alpha=0.5, zorder=3)
        # ax_2.scatter(scatter_ep_time, scatter_ep_amp, color='pink', zorder=4)
        # # ax_1.set_xlim([5, 30])
        # ax_2.set_ylabel('power')
        # ax_2.set_xlabel('time [sec]')
        # ax_2.spines['right'].set_visible(False)
        # ax_2.spines['top'].set_visible(False)
        # ax_2.get_xaxis().tick_bottom()
        # ax_2.get_yaxis().tick_left()
        # plt.savefig(file_path + r'Hilbert_transform_just_pos_w_peaks_channel_wo_raw_' + str(wanted_labels[idx]))
        # plt.clf()
        # plt.show()
        # ax_2.plot(t, power_sum)
        # ax_2 = plt.subplot(312, sharex=ax_1)

        # # ax_2.plot(t, np.angle(channel))
        # ax_2.set_xlim([7, 12.5])
        # ax_2.set_ylabel('angle')
        # ax_2.set_xlabel('time [sec]')
        # ax_3 = plt.subplot(212, sharex=ax_1)
        #
        # # ax_3.plot(t, np.abs(channel))
        # ax_3.set_xlim([7.5, 12.5])
        # ax_3.set_ylabel('amplitude')


