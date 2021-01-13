import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import h5py


def get_channel_id(current_label):
    for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if current_label == ch[4].decode('utf8'):
            return ch[1]


mea_recording_path = "/home/lisa_ruth/mea_recordings/CSD_data/h5_data" \
                     "/2020-10-13T14-27-38FHM3_GS967_BL6_P15_male_400ms_7psi_Slice3_Test1_WITH.h5"

relevant_labels = ['C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'E3', 'E4',
                   'E5', 'E6', 'E7', 'E8', 'E9', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G3', 'G4', 'G5', 'G6',
                   'G7', 'G8', 'G9', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9',
                   'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'M3', 'M4', 'M5',
                   'M6', 'M7', 'M8', 'M9', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9']

mea_file = h5py.File(mea_recording_path, 'r')
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
sampling_rate = 10000
for idx, label in enumerate(relevant_labels):
    id = get_channel_id(label)
    signal = voltage_trace_snippet = voltage_traces[id][:875000]    # time = length of csd video
    f, t, Sxx = scipy.signal.spectrogram(signal, sampling_rate)
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylim(0, 100)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.savefig('spectogram_' + str(idx) + '.png')
    plt.close()
    print('spectogram', idx, 'saved')

    freqs, psd = signal.welch(signal)

    plt.figure(figsize=(5, 4))
    plt.semilogx(freqs, psd)
    plt.title('PSD: power spectral density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.tight_layout()
    plt.savefig('PSD_' + str(idx) + '.png')
    plt.close()
    print('PSD', idx, 'saved')

