import h5py
import numpy as np
from IPython import embed

path = r'G:\Lisa\data\data\Daniela GS967\MEA\200506\2020-05-06T12-40-44Slice1 Test1_BL6 FHM3 P19_coronal_400ms 8psi.meae'

file = h5py.File(path, 'r')
# print(file.keys())
embed()