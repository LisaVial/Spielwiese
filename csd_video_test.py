import h5py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import time

mea_recording_path = '../../mea_recordings/CSD_data/h5_data/' \
                     '2020-10-13T11-24-12FHM3_GS967_BL6_P15_male_400ms_7psi_Slice1_Test1.h5'
video_path = '../../mea_recordings/CSD_data/' \
             '201013_microscope/FHM3_GS967_BL6_P15_male_exp100ms_dur100sec_400ms_7psi_Slice1_Test1.tif'

mea_file = h5py.File(mea_recording_path, 'r')
t0 = time.time()
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
t1 = time.time() - t0
print('time to load traces:', t1)

t2 = time.time()
dataset = Image.open(video_path)
print(dataset.shape)
t3 = time.time() - t2
print('time to open tiff stack:', t3)
plt.imshow(dataset[0])
plt.show()
