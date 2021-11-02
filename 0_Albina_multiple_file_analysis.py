import h5py
import glob
import numpy as np
from circus.shared.parser import CircusParser
import matplotlib.pyplot as plt
from IPython import embed
import seaborn as sns


def get_bursts(all_spiketimes):
    all_bursts = []
    max_spike_time_diff = 0.1  # s
    min_spikes_per_burst = 3

    burst_counter = 0
    for channel_spiketimes in all_spiketimes:
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
                        burst_counter += 1
                    # keep all spikes in list that are close enough to current spike
                    current_burst_indices = [current_spike_index]


            # end of for current_spike_index in range(len(channel_spiketimes)):
            # don't forget to add last burst
            if len(current_burst_indices) >= min_spikes_per_burst:
                # at least 3 spikes in final burst list -> this is a burst, too
                for burst_spike_index in current_burst_indices:
                    channel_burst_indices.add(burst_spike_index)
                burst_counter += 1

        # at this point, all the channels' bursts are in bursts list
        burst_spike_index_list = list(channel_burst_indices)  # set -> list
        burst_spike_index_list.sort()

        all_bursts.append(burst_spike_index_list.copy())

    return all_bursts, burst_counter


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


import os


def get_folder_infos(path):
    '''returns list of tuples (folder_name, spike_file_name, filter_file_name, date, time, tags, version)'''
    current_working_directory = os.getcwd()
    os.chdir(path)

    os_walk_data = next(os.walk('.'))
    folder_names = os_walk_data[1]
    file_names = os_walk_data[2]
    folder_infos = []

    for folder_name in folder_names:
        if not 'Control' in folder_name:
            continue

        files_in_folder = next(os.walk(path + folder_name))[2]
        if len(files_in_folder) == 0:
            print("Skipping empty folder", folder_name)
            continue

        spike_file_name = [file_name for file_name in files_in_folder if file_name.endswith('.clusters.hdf5')][0]

        filter_file_name = ""
        filter_file_names = [file_name for file_name in file_names if file_name == folder_name + '.h5']
        if len(filter_file_names) > 0:
            filter_file_name = filter_file_names[0]
        else:
            # try with blank at end of folder name
            filter_file_names = [file_name for file_name in file_names if file_name == folder_name + ' .h5']
            if len(filter_file_names) > 0:
                filter_file_name = filter_file_names[0]

        date = folder_name[:10]
        time = folder_name[11:19]
        tags = [token.strip() for token in folder_name[26:].split('+') if len(token.strip()) > 0]

        # remove _slice 2 as tag
        while '_slice2' in tags:
            tags.remove('_slice2')

        # remove slice2 from all tags
        for index, tag in enumerate(tags):
            if tag.endswith(' slice2'):
                tags[index] = tag[:-len(' slice2')].strip()

        if len(tags) > 0 and len(tags[0]) == 1:
            version = tags[0]
            tags = tags[1:]
        else:
            version = ""

        folder_infos.append((folder_name, spike_file_name, filter_file_name, date, time, tags, version))

    os.chdir(current_working_directory)
    return folder_infos


path = r'/home/lisa_ruth/spyking-circus/'
folder_infos = get_folder_infos(path)
# 0           1                2                3       4    5     6
#(folder_name, spike_file_name, filter_file_name, date, time, tags, version)


group_map = dict()
for fi in folder_infos:
    date = fi[3]
    version = fi[6]
    if date not in group_map.keys():
        group_map[date] = dict()
    if version not in group_map[date].keys():
        group_map[date][version] = []

    group_map[date][version].append(fi)


for date in sorted(group_map.keys()):
    print(date)
    for version in sorted(group_map[date].keys()):
        print('version', version)

        figure_name = '/mnt/Data/Albina/' + date + 'burst_count_comparison_logy' + version + '.png'
        overall_spikes = []
        overall_bursts = []

        fis = sorted(group_map[date][version])

        tick_labels = []
        for fi in fis:
            tags = fi[5]
            if len(tags) == 0:
                tick_labels.append("Control")
            elif len(tags) == 1:
                tick_labels.append(tags[0])
            elif len(tags) == 2:
                tick_labels.append('+ ' + tags[1])
            elif len(tags) >= 3:
                tick_labels.append('+ ' + tags[2] + ' +' + tags[3])

        for fi in fis:

            file = os.path.join(path, fi[0], fi[1])  # spike file
            filter_file = os.path.join(path, fi[2])
            print(file)

            current_file = h5py.File(file, 'r')
            params = CircusParser(filter_file)

            spike_indices = retrieve_spiketimes(current_file)
            sorted_spike_indices = [np.sort(spike_indices[m]) for m in range(len(spike_indices))]
            sampling_rate = float(params.get('data', 'sampling_rate'))
            spiketimes = np.array(spike_indices, dtype=object) / sampling_rate
            sorted_spiketimes = [np.sort(spiketimes[i]) for i in range(len(spiketimes))]
            num_of_spikes = [len(spike_ls) for spike_ls in sorted_spiketimes]
            num_of_spikes = np.sum(num_of_spikes)
            overall_spikes.append(num_of_spikes)
            all_burst, burst_counter = get_bursts(sorted_spiketimes)
            print(burst_counter)
            # num_of_burst_spikes = [len(burst_ls) for burst_ls in all_burst]
            # num_of_burst_spikes = np.sum(num_of_burst_spikes)
            # embed()
            overall_bursts.append(burst_counter)

        sns.set()
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111)
        ax.plot(range(len(overall_spikes)), overall_spikes, '--o', color='k', label='spikes')
        ax.plot(range(len(overall_spikes)), overall_bursts, '--o', color='#7fb6bd', label='bursts')
        # ax.set_yscale('log')
        ax.set_xticks(range(len(overall_bursts)))
        ax.set_xticklabels(tick_labels, fontsize=14)
        ax.set_ylabel(r'count', fontsize=14)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.tick_params(labelsize=12, direction='out')
        fig.legend()
        fig.tight_layout()
        plt.savefig(figure_name)

        print('figure saved')
