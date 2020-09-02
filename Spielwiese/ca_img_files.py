import h5py
from IPython import embed
import csv
import pandas as pd
import numpy as np

path = r'G:\Lisa\data\Niko'
file = r'\STD_Cortex 10x 20fps gain 2.h5'
file_csv = r'\STD_Cortex 10x 20fps gain 2_MMStack_Default.ome-1.csv'
f = h5py.File(path+file, 'r')
with open(path+file_csv, 'rb') as f_input:
    csv_input = csv.reader(f_input)
    header = next(csv_input)
    data = zip([map(int, row) for row in csv_input])
print(data)
dset = f['t0']['channel0']
embed()
exit()
print(dset.shape)
# for i in range(dset.shape[0]):
#     print('column: ', i)
#     for j in range(dset.shape[1]):
#         print(dset[i, j])
