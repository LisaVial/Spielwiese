import h5py
import numpy as np
from IPython import embed

filepath = '/mnt/Data/Lisa/human/15-07-2021/' \
           '2021-07-15T16-40-00_human_organotypic_Slice2_baseline.h5'

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
for ch_id, geo in zip(np.array(ch_ids)[indices], np.array(geometry)):
    geometry_probe[ch_id] = tuple(geo)
print(geometry_probe)
fout = "probe.txt"
fo = open(fout, "w")

ch_ids_out = 'ch_ids.txt'
fo_ch_ids = open(ch_ids_out, 'w')

for k, v in geometry_probe.items():
    fo.write(str(k) + ': ' + str(v) + ', \n')
    fo_ch_ids.write(str(k) + ', ')

fo.close()
print('probe file saved...')

fo_ch_ids.close()
print('channel ids saved...')

#
# print(sorted_channel_ids-2)
# savedict.write(str(geometry_probe))
# savedict.close()
