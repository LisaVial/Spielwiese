import numpy as np


def isivec(spiketimes):
    isivec = []
    for i in range(len(spiketimes)):
        difftimes = np.diff(spiketimes[i])
        isivec.append(difftimes)

    return isivec