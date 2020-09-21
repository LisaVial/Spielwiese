import h5py
from IPython import embed


test = [[1, 2, 3, 4], [5, 6, 7, 8]]
filename = 'test_file.h5'

with h5py.File(filename, 'w') as f:
    dset = f.create_dataset('test', dtype='i', data=test)

f = h5py.File(filename, 'r')
embed()
