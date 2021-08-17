import h5py
import numpy as np
from IPython import embed

filepath = '/home/lisa_ruth/mea_recordings/Daniela_h5/MEA_210217/' \
           '2021-02-17T10-52-47FHM3_GS967_BL6_P16_female_400ms_7psi_Slice1_Test1.h5'

file = h5py.File(filepath, 'r')

labels = [ch[4].decode('utf8') for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
# ToDo: recheck if strings are created correctly
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ch_ids = [ch[1] for ch in file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
indices = list(np.argsort(same_len_labels))
sorted_channel_ids = np.array(ch_ids)[indices]
# check spacing, probably 200 um and radius of 30
# spacing = 38
spacing = 200
# # radius = 4
# diameter = 30

geometry = []

for i in range(16):
    for j in reversed(range(16)):
        if (i == 0 and j == 0) or (i == 0 and j == 15) or (i == 15 and j == 0) or (i == 15 and j == 15):
            continue
        x = i * spacing
        y = j * spacing

        current_electrode = (x, y)
        geometry.append(current_electrode)

geometry_probe = dict()
for ch_id, geo in zip(np.array(ch_ids)[indices], np.array(geometry)[indices]):
    geometry_probe[ch_id] = tuple(geo)

fout = "probe.txt"
fo = open(fout, "w")

for k, v in sorted(geometry_probe.items()):
    fo.write(str(k) + ': ' + str(v) + ', \n')

fo.close()
print('probe file saved...')


#
# print(sorted_channel_ids-2)
# savedict.write(str(geometry_probe))
# savedict.close()
