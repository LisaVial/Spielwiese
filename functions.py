import numpy as np


def get_ordered_indices(h5_file):
    '''
    This function returns an array of ordered indices for the MEA 252 setup
    :param h5_file: converted, raw .h5 file
    :return: indices: indices to go through mcs mea files in the order of channels (A02 - R15)
    '''
    labels = [ch[4].decode('utf8') for ch in h5_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
    same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
    indices = list(np.argsort(same_len_labels))
    return indices


def isivec(spiketimes):
    isivec = []
    for i in range(len(spiketimes)):
        difftimes = np.diff(spiketimes[i])
        isivec.append(difftimes)

    return isivec