import scipy.signal
import matplotlib.pyplot as plt
import numpy as np
import h5py
from IPython import embed


def get_channel_id(current_label):
    for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if current_label == ch[4].decode('utf8'):
            return ch[1]


mea_recording_path = "/home/lisa_ruth/mea_recordings/Niko/MEA_recordings/20210125 P15 cortical (Syn-gCamp7f)/" \
                     "2021-01-25T12-03-59Slice2_0Mg2+_10mMNMDAPuffing_7psi_600ms_2pulses_3sgap.h5"

# relevant_labels = ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
#                    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
#                    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
#                    'F9', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
#                    'H8', 'H9', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6',
#                    'K7', 'K8', 'K9', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'M1', 'M2', 'M3', 'M4', 'M5',
#                    'M6', 'M7', 'M8', 'M9', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'O1', 'O2', 'O3',
#                    'O4', 'O5', 'O6', 'O7', 'O8', 'O9', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'R2',
#                    'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']

# relevant_labels = ['F4', 'F5', 'F6', 'F7', 'F8', 'G4', 'G5', 'G6', 'G7', 'G8', 'H4', 'H5', 'H6', 'H7', 'H8', 'J4', 'J5',
#                    'J6', 'J7', 'J8', 'K4', 'K5', 'K6', 'K7', 'K8', 'L4', 'L5', 'L6', 'L7', 'L8', 'M4', 'M5', 'M6', 'M7',
#                    'M8', 'N4', 'N5', 'N6', 'N7', 'N8', 'O4', 'O5', 'O6', 'O7', 'O8', 'R4', 'R5', 'R6', 'R7', 'R8']

relevant_labels = ['A2', 'J2', 'L2', 'L5']

mea_file = h5py.File(mea_recording_path, 'r')
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
sampling_rate = 10000
conversion_factor = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
exponent = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6 #6 = pV -> uV
for idx, label in enumerate(relevant_labels):
    id = get_channel_id(label)
    signal = voltage_trace_snippet = voltage_traces[id][:879000] # only the duration of csd video
    scaled_snippet = signal * conversion_factor * np.power(10.0, exponent)
    f, t, Sxx = scipy.signal.spectrogram(scaled_snippet, sampling_rate, nperseg=2**10, noverlap=2**8)
    # f, t, Sxx = scipy.signal.spectrogram(signal, sampling_rate, nperseg=2**10, noverlap=2**8)
    # embed()
    plt.pcolormesh(t, f, Sxx, shading='gouraud', vmin=0, vmax=3)
    # plt.ylim(0, 100)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    # plt.savefig('spectogram_' + str(label) + '.png')
    plt.show()
    # embed()
    print('figure', idx, 'of', len(relevant_labels), 'saved')

    # freqs, psd = scipy.signal.welch(signal, fs=10000)
    #
    # plt.figure(figsize=(5, 4))
    # plt.semilogx(freqs, psd)
    # plt.title('PSD: power spectral density')
    # plt.xlabel('Frequency')
    # plt.ylabel('Power')
    # plt.tight_layout()
    # plt.savefig('PSD_' + str(idx) + '.png')
    # plt.close()
    # print('PSD', idx, 'saved')
    #
