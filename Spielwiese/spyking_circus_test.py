import h5py
import matplotlib.pyplot as plt
from IPython import embed


file_path = r'D:\Lisa\spyking_circus_test\2020-06-05T11-25-32AAV5-KCl8mM\2020-06-05T11-25-32AAV5-KCl8mM.result.hdf5'

file = h5py.File(file_path, 'r')

spiketime_channels = list(file['spiketimes'].keys())

for channel in spiketime_channels:
    plt.eventplot(file['spiketimes'][channel])
    plt.show()
    plt.savefig('spiketimes_' + channel + '.png')
# embed()
