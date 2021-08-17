import h5py

import matplotlib.pyplot as plt


mea_recording_path = "/home/lisa_ruth/mea_recordings/second_movie" \
                     "/2020-08-26T14-49-54FHM3_GS967_BL6_P19_male_400ms_7psi_Slice3_Test1_WITH.h5"

mea_file = h5py.File(mea_recording_path, 'r')
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
for idx, voltage_trace in enumerate(voltage_traces):
    print(idx)
    plt.plot(voltage_trace)
    plt.show()