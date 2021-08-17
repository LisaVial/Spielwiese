from scipy.io import loadmat
import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy as np

data = loadmat('ANDA2021_Spectral_DataSets.mat')

flickr_data = data['flicker_signals']
V1_lfps = data['V1_lfp']
V4_lfp = data['V4_lfp']
print(V4_lfp.shape)