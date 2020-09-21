import h5py
import numpy as np
from IPython import embed

filepath = r'D:\Lisa\data\Andrea\AAV5-CamKII-PSAM-HA\Slice 1\2020-06-16T13-11-53AAV5PSAMCamIIGFP KCl9.6mM.h5'

file = h5py.File(filepath, 'r')

labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[0] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
indices = list(np.argsort(same_len_labels))

spacing = 38
radius = 4

geometry = []

for i in range(16):
    for j in range(16):
        if i == 0 and j == 0 or i == 0 and j == 15 or i == 15 and j == 0 or i == 15 and j == 15:
            continue
        x = radius + i * spacing
        y = radius + j * spacing

        current_electrode = (x, y)
        geometry.append(current_electrode)

embed()