import numpy as np
import h5py
from IPython import embed

abs_path = r'C:\Users\Imaris\Desktop\Lisa\data\Andrea\AAV5\2020-06-05T11-25-32AAV5-KCl8mM.h5'

with h5py.File(abs_path, 'r') as hdf:
    ls = list(hdf.keys())
    print(' List of datasets in this file: \n', ls)
    data = hdf.get('Data')
    raw_data = data['Recording_0']['AnalogStream']['Stream_0']['ChannelData']
    embed()
    print(raw_data.shape)
    # print(raw_data[0])