import h5py
import numpy as np
import glob


def get_scaled_channel(voltage_trace):
    conversion_factor = mcs_file['Data/Recording_0/AnalogStream/Stream_0/InfoChannel'][0]['ConversionFactor']
    exponent = mcs_file['Data/Recording_0/AnalogStream/Stream_0/InfoChannel'][0]['Exponent'] + 6
    # 6: pV -> uV
    scaled_trace = voltage_trace * conversion_factor * np.power(10.0, exponent)
    return scaled_trace


mcs_h5_filepath = '/home/lisa_ruth/Lisa/human/2021-06-22T16-11-39human_slices_Slice1_Vareniclin_washin.h5'

mcs_file = h5py.File(mcs_h5_filepath, 'r')
voltage_traces = mcs_file['Data/Recording_0/AnalogStream/Stream_0/ChannelData'][:]
ids = [ch[0] for ch in mcs_file['Data/Recording_0/AnalogStream/Stream_0/InfoChannel']]
labels = [ch[4].decode('utf8') for ch in mcs_file['Data/Recording_0/AnalogStream/Stream_0/InfoChannel']]
same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
ordered_indices_for_ids = list(np.argsort(same_len_labels))
# ordered_indices_for_ids = [ordered_indices_for_ids[3], ordered_indices_for_ids[4], ordered_indices_for_ids[18],
#                            ordered_indices_for_ids[19]]

scaled_traces = []
for i in ordered_indices_for_ids:
    print(labels[i])
    scaled_trace = get_scaled_channel(voltage_traces[i])
    scaled_traces.append(scaled_trace)

h5_filename = mcs_h5_filepath[:-3] + '_rdy_4_SC.h5'
print(h5_filename)

with h5py.File(h5_filename, 'w') as hf:
    dset_1 = hf.create_dataset('scaled', data=scaled_traces)

print(h5_filename, 'file saved...')
