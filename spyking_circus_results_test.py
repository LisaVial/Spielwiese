import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
from IPython import embed
import os
from matplotlib.cm import get_cmap

path = r'E:\0_PhD\data\2020-06-05T12-31-47AAV5-KCl8mM-washed out'
filename = r'\2020-06-05T12-31-47AAV5-KCl8mM-washed out.result.hdf5'

file = h5py.File(path+filename, 'r')
keys = list(file.keys())
st_keys = list(file[keys[2]].keys())

same_len_keys = []

for k in st_keys:
    if len(k) == 6:
        longer_key = str(k[:5]) + '00' + str(k[-1])
        same_len_keys.append(longer_key)
    elif len(k) == 7:
        longer_key = str(k[:5]) + '0' + str(k[-2:])
        same_len_keys.append(longer_key)
    else:
        same_len_keys.append(k)
colors = ['#006d7c', '#3b0089', '#94c100', '#00c4e0', '#6301e5', '#c0fb00', '#008699', '#4900aa', '#b7ee00', '#005561',
          '#2e006c', '#749800', '#003b43', '#20004a', '#20004a']
colors = colors * int(np.ceil(len(st_keys)/len(colors)))
for i in range(int(file['info']['duration'][0] / 60)):
    fig = plt.figure()
    for idx, key in zip(reversed(range(len(st_keys))), np.array(st_keys)[np.argsort(same_len_keys)]):
        spike_indices = file['spiketimes'][key][:]
        spiketimes = spike_indices / 10000
        if len(spike_indices) >= 1:
            if i == 0:
                mask = ((i <= spiketimes) & (spiketimes < i+1))
                to_plot = spiketimes[mask]

                plt.scatter(to_plot, np.ones(len(to_plot)) * idx, marker='|', c=colors[idx])
            elif i == 32:
                mask = (i <= spiketimes)
                to_plot = spiketimes[mask]

                plt.scatter(to_plot, np.ones(len(to_plot))*idx, marker='|', c=colors[idx])
            else:
                mask = ((i <= spiketimes) & (spiketimes < i + 1))
                to_plot = spiketimes[mask]

                plt.scatter(to_plot, np.ones(len(to_plot)) * idx, marker='|', c=colors[idx])
        else:
            print('No spikes found in channel ', idx)
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    fig.savefig('AAV5-KCl8mM-washed out_spikes_' + str(i) + '.png')
    print(i, 'figure saved')
    plt.close()

print('saved %i' %i, ' figures.')
