import h5py
import matplotlib.pyplot as plt
import numpy as np
from IPython import embed


path = r'D:\Lisa\spyking_circus_test\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi'
filename = r'\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.result.hdf5'

file = h5py.File(path+filename, 'r')
# plt.plot(file['proj'][:])
# plt.show()
embed()