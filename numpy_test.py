import numpy as np
import tables as tb
import h5py
import os
import time
from IPython import embed


def get_channel_id(label):
    for ch in raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if label == ch[4].decode('utf8'):
            return ch[1]


def get_channel_labels(pad_with_zero=False):
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


column_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R']

# split path and filename to be able to create new directory more easily
raw_file_dir = r'/mnt/Data/Lisa/human/22-06-2021/'
raw_file_name = r'2021-06-22T15-51-27human_slices_Slice1_BL.h5'

# change directory to the folder where the file can be found in
os.chdir(raw_file_dir)

# check if directory with filename exists. if so, go to new directory, else make a new directory with the same name
# as the filename
if os.path.isdir(raw_file_name.split('.')[0]):
    os.chdir(raw_file_name.split('.')[0])
else:
    os.mkdir(raw_file_name.split('.')[0])

# open hdf5 file and iterate through voltage traces, also check how much time it needs
time_1 = time.time()
h5file = tb.open_file(os.path.join(raw_file_dir, raw_file_name), driver="H5FD_CORE")
# h5 = h5file.root
# traces = h5['Data/Recording_0/AnalogStream/Stream_0/ChannelData'][:]
raw_file = h5py.File(os.path.join(raw_file_dir, raw_file_name), 'r')
traces = raw_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
time_2 = time.time()
print('opening hdf5 file takes', time_2-time_1, 's')
# # embed()
time_3 = time.time()
labels = get_channel_labels()
row_indices = []
for label in labels:
    row_idx = get_channel_id(label)
    row_indices.append(row_idx)
time_4 = time.time()
print('It takes', time_4-time_3, 's to get row indices')
time_5 = time.time()
time_6 = time.time()
print('It takes', time_6 - time_5, 's to open a voltage traces in a HDF5 file')

for i, ri in enumerate(row_indices):
    time_7 = time.time()
    trace = np.array(traces[ri], dtype=np.float32)
    filename = 'raw_trace_' + labels[i] + '.npy'
    np.save(filename, trace)
    time_8 = time.time()
    print('It takes', time_8 - time_7, 's to reference & save trace')
# embed()
