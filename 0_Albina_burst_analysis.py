import matplotlib.pyplot as plt
import numpy as np
import h5py
import re
from scipy import signal
from circus.shared.parser import CircusParser
from IPython import embed
import gc


def get_mcs_index(sc_index: int, dead_channels: list):

    # special case: sc index is 0 and mcs index 0 is not a dead channel
    if 0 not in dead_channels and sc_index == 0:
        return 0

    current_sc_index = 0
    for row_index in range(252):
        if row_index not in dead_channels:
            current_sc_index += 1
            if current_sc_index == sc_index:
                return row_index

    raise Exception("SC index not in valid range (0, " + str(251 - len(dead_channels)) + ")")


def scale_trace(trace_to_scale, filter_file):
    vt = trace_to_scale
    conversion_factor = \
        filter_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
    exponent = filter_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6
    # 6 = pV -> uV
    scaled_trace = vt * conversion_factor * np.power(10.0, exponent)
    return scaled_trace


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


def get_channel_labels(pad_with_zero=True):
    labels = [ch[4].decode('ascii') for ch in
              filter_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    return labels


def get_sc_index(mcs_index: int, dead_channels: list):

    if mcs_index in dead_channels:
        raise Exception("MCS index is a dead channel and has no SC index")

    sc_index = 0
    for row_index in range(252):

        if row_index == mcs_index:
            return sc_index

        if row_index not in dead_channels:
            sc_index += 1

    raise Exception("MCS index not in valid range (0, 251)")


def get_label_for_mcs_index(mcs_index: int, ordered_mcs_indices: list, pad_with_zero: bool = False):
    return get_channel_labels(pad_with_zero)[ordered_mcs_indices.index(mcs_index)]


def get_label_for_sc_index(sc_index: int, dead_channels: list, ordered_mcs_indices: list,
                            pad_with_zero: bool = False):
    return get_label_for_mcs_index(get_mcs_index(sc_index, dead_channels), ordered_mcs_indices, pad_with_zero)


# CHANGE PATHS TO ANALYZE DIFFERENT FILES
filtered_filepath = r'/mnt/Data/Albina/data from home/2021-06-29T12-05-34Control_slice2.h5'
result_filepath = r'/mnt/Data/Albina/data from home/2021-06-29T12-05-34Control_slice2/' \
                  r'2021-06-29T12-05-34Control_slice2.clusters.hdf5'

filter_file = h5py.File(filtered_filepath, 'r')
result_file = h5py.File(result_filepath, 'r')
params = CircusParser(filtered_filepath)

filter_file_voltage_traces = filter_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
ch_ids = [ch[1] for ch in filter_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
spike_indices = retrieve_spiketimes(result_file)
sorted_spike_indices = [np.sort(spike_indices[m]) for m in range(len(spike_indices))]
sampling_rate = float(params.get('data', 'sampling_rate'))
spiketimes = np.array(spike_indices, dtype=object)/sampling_rate
sorted_spiketimes = [np.sort(spiketimes[i]) for i in range(len(spiketimes))]
spike_differences = [np.diff(sorted_spiketimes[j]) for j in range(len(sorted_spiketimes))]
burst_indices = [np.where(spike_differences[m] < 0.1)[0] for m in range(len(spike_differences))]

max_spike_time_diff = 0.1 #s
min_spikes_per_burst = 3

all_labels = get_channel_labels()

all_bursts = []

for channel_spiketimes in sorted_spiketimes:
    if len(channel_spiketimes) < min_spikes_per_burst:
        continue  # skip channels with less spikes than necessary

    channel_burst_indices = set()  # spike times in burst for this channel
    current_burst_indices = []  # records spike times to find potential burst

    for current_spike_index in range(len(channel_spiketimes)):

        if len(current_burst_indices) == 0:
            current_burst_indices.append(current_spike_index)
        else:  # at least one spike time in list
            first_spike_time_index = current_burst_indices[0]
            first_spike_time = channel_spiketimes[first_spike_time_index]

            current_spike_time = channel_spiketimes[current_spike_index]

            if (current_spike_time - first_spike_time) <= max_spike_time_diff:
                # current spike is within burst window -> add to list and continue
                current_burst_indices.append(current_spike_index)
            else:
                # current spike is no longer in burst window
                if len(current_burst_indices) >= min_spikes_per_burst:
                    # at least 3 spikes -> this is a burst
                    for burst_index in current_burst_indices:
                        channel_burst_indices.add(burst_index)

                # # keep all spikes in list that are close enough to current spike
                # current_burst_indices = [index for index in current_burst_indices
                #                                     if (current_spike_time - channel_spiketimes[index])
                #                                     <= max_spike_time_diff]
                # # don't forget to add current spike time index to list as well
                current_burst_indices = [current_spike_index]
                # current_burst_indices.append(current_spike_index)

    # end of for current_spike_index in range(len(channel_spiketimes)):
    # don't forget to add last burst
    if len(current_burst_indices) >= min_spikes_per_burst:
        # at least 3 spikes in final burst list -> this is a burst, too
        for burst_spike_index in current_burst_indices:
            channel_burst_indices.add(burst_spike_index)

    # at this point, all the channels' bursts are in bursts list
    burst_spike_index_list = list(channel_burst_indices)  # set -> list
    burst_spike_index_list.sort()
    all_bursts.append(burst_spike_index_list.copy())

# end of for channel_spiketimes in sorted_spiketimes:

regular_expression = '{\s*1\s*:\s*\[(.*?)?\]\s*\}'
pattern = re.compile(regular_expression)

dead_channels_string = params.get('detection', 'dead_channels')
match_object = pattern.match(dead_channels_string)
if match_object:
    channel_list_string = match_object.group(1)
    dead_channels = [int(ch) for ch in channel_list_string.split(',')]
else:
    dead_channels = []

print('iterating through voltage traces...')
for idx, voltage_trace in enumerate(filter_file_voltage_traces):
    label = get_label_for_sc_index(idx, dead_channels, ch_ids)
    filename = '0_raw_trace_spikes_and_bursts_' + label + '.png'
    fig_raw = plt.figure(figsize=(12, 9))
    ax_raw = fig_raw.add_subplot(111)
    print('Setting up time array...')
    time = np.arange(0, len(voltage_trace)/sampling_rate, 1 / sampling_rate)
    scaled_trace = scale_trace(voltage_trace, filter_file)
    ax_raw.plot(time, scaled_trace, zorder=1)
    ax_raw.set_xlim(0, time[-1])
    ax_raw.set_xlabel('time [s]', fontsize=14)
    ax_raw.set_ylabel(r'voltage [$\mu\,$V]', fontsize=14)
    ax_raw.spines['right'].set_visible(False)
    ax_raw.spines['top'].set_visible(False)
    ax_raw.get_xaxis().tick_bottom()
    ax_raw.get_yaxis().tick_left()
    ax_raw.tick_params(labelsize=12, direction='out')
    if idx not in dead_channels:
        sc_index = get_sc_index(idx, dead_channels)
        spike_indices_channel = sorted_spike_indices[sc_index]
        scatter_time = []
        scatter_amps = []
        burst_time = []
        burst_amps = []

        for jdx, si_idx in enumerate(spike_indices_channel):
            if jdx in all_bursts[idx]:
                burst_time.append(time[si_idx])
                burst_amps.append(scaled_trace[si_idx])
            else:
                scatter_time.append(time[si_idx])
                scatter_amps.append(scaled_trace[si_idx])

        ax_raw.scatter(burst_time, burst_amps, color='red', zorder=2)
        ax_raw.scatter(scatter_time, scatter_amps, color='k', zorder=2)
    fig_raw.savefig('/mnt/Data/Albina/' + filename)
    print('saved figure', idx+1, 'of', len(filter_file_voltage_traces))
    plt.close()
    gc.collect()
    # fig_raw.savefig('/mnt/Data/Albina/raw_trace_plot_with_scatter_spikes_and_bursts_w_xlim.png')
