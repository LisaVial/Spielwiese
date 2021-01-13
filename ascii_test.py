import matplotlib.pyplot as plt
from scipy import signal

file_path = r'E:\FHM3_GS967_BL6_P17_female_400ms_7psi_Slice3_Test2_WITH.txt'

f = open(file_path, 'r')
indices = []
time = []
v_1 = []
v_2 = []
for i, line in enumerate(f):
    line = line.strip()
    columns = line.split(', ')
    if i >= 3 and len(columns) > 1:
        indices.append(float(columns[0]))
        time.append(float(columns[1]))
        v_1.append(float(columns[2]))
        v_2.append(float(columns[4]))

print(indices, '\n', time, '\n', v_1, '\n', v_2)
b, a = signal.iirnotch((50 / (20000/2)), 20000)
v_1_notch = signal.filtfilt(b, a, v_1)
v_2_notch = signal.filtfilt(b, a, v_2)
plt.plot(time[:2000], v_1[:2000])
plt.plot(time[:2000], v_1_notch[:2000])
plt.plot(time[:2000], v_2[:2000])
plt.plot(time[:2000], v_2_notch[:2000])
plt.show()
