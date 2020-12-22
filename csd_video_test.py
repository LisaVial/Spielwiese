import h5py
import matplotlib
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
import time
matplotlib.use("agg")


def get_distance(label_a, label_b):
    columns = [ord(label_a[0]), ord(label_b[0])]

    # there is no 'I' column -> adapt all indices after 'I'
    if columns[0] > ord('I'):
        columns[0] -= 1
    if columns[1] > ord('I'):
        columns[1] -= 1

    col_diff = columns[1] - columns[0]

    rows = int(label_a[1:]), int(label_b[1:])
    row_diff = rows[1] - rows[0]

    return col_diff, row_diff


def calculate_plot_positions(reference_label, x0, y0, x_offset, y_offset, relevant_labels):
    positions = dict()

    for label in relevant_labels:
        col_diff, row_diff = get_distance(reference_label, label)
        positions[label] = (x0 + col_diff * x_offset, y0 + row_diff * y_offset)

    return positions


def get_channel_id(label):
    for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if label == ch[4].decode('utf8'):
            return ch[1]


mea_recording_path = r'C:\Users\Lisa\Desktop\mea_csd\h5_data' \
                     r'\2020-10-13T14-27-38FHM3_GS967_BL6_P15_male_400ms_7psi_Slice3_Test1_WITH.h5'
video_path = r'C:\Users\Lisa\Desktop\mea_csd\201013_microscope' \
             r'\FHM3_GS967_BL6_P15_male_exp100ms_dur100sec_400ms_7psi_Slice3_Test1_WITH_4movie.tif'

mea_file = h5py.File(mea_recording_path, 'r')
t0 = time.time()
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
t1 = time.time() - t0
print('time to load traces:', t1)
# ids = [ch[1] for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
# labels = [ch[4].decode('utf8') for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']]
# same_len_labels = [str(label[0]) + '0' + str(label[1]) if len(label) < 3 else label for label in labels]
# ordered_indices = list(np.argsort(same_len_labels))

# channel_ids = list(np.asarray(ids)[ordered_indices])
# print(channel_ids[49], labels[channel_ids[49]])

t2 = time.time()
# retvals, mats = cv2.imreadmulti(video_path, flags=(cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH))
mats = tiff.imread(video_path)
t3 = time.time() - t2
print('time to open tiff stack:', t3)
print(mats.shape)

relevant_labels = ['C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'E3',  'E4',
                   'E5', 'E6', 'E7', 'E8', 'E9', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',  'G3', 'G4', 'G5', 'G6',
                   'G7', 'G8', 'G9', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9',
                   'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'M3', 'M4', 'M5',
                   'M6', 'M7', 'M8', 'M9', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9']
label = 'C3'
x0, y0 = (0.175, 0.75)
x_offset, y_offset = (0.06, -0.09)
plot_positions = calculate_plot_positions(label, x0, y0, x_offset, y_offset, relevant_labels)

stepsize = 1000
num_frames = len(mats)
timepoints = np.arange(stepsize, (num_frames * stepsize) + 1, stepsize)

for i, mat in enumerate(mats):
    if i < 317:
        continue
    fig = plt.figure(figsize=(12, 8))
    plt.imshow(mat, cmap='gray', interpolation='none')
    # ax_0 = fig.add_axes([0.205, 0.6725, 0.05, 0.05])
    # ax_0.plot(voltage_traces[channel_ids[33]][:1000], alpha=0.25)
    # ax_0.spines['right'].set_visible(False)
    # ax_0.spines['top'].set_visible(False)
    # ax_0.spines['left'].set_visible(False)
    # ax_0.spines['bottom'].set_visible(False)
    # ax_0.axes.get_xaxis().set_visible(False)
    # ax_0.axes.get_yaxis().set_visible(False)
    # ax_0.axes.get_xaxis().set_ticks([])
    # ax_0.axes.get_yaxis().set_ticks([])
    # ax_0.patch.set_alpha(0.0)
    #
    # ax_1 = fig.add_axes([0.205, 0.5725, 0.05, 0.05])
    # ax_1.plot(voltage_traces[channel_ids[34]][:1000], alpha=0.25)
    # ax_1.spines['right'].set_visible(False)
    # ax_1.spines['top'].set_visible(False)
    # ax_1.spines['left'].set_visible(False)
    # ax_1.spines['bottom'].set_visible(False)
    # ax_1.axes.get_xaxis().set_visible(False)
    # ax_1.axes.get_yaxis().set_visible(False)
    # ax_1.axes.get_xaxis().set_ticks([])
    # ax_1.axes.get_yaxis().set_ticks([])
    # ax_1.patch.set_alpha(0.0)
    if i > 0:
        print(timepoints[i-1], timepoints[i])
    for label in plot_positions.keys():
        position = plot_positions[label]
        id = get_channel_id(label)
        ax_x = fig.add_axes([position[0], position[1], 0.05, 0.05])
        if i == 0:
            ax_x.plot(voltage_traces[id][:int(timepoints[i])], alpha=0.25, color='white')
            ax_x.text(position[0], position[1], label, color='white', fontsize=8)
        ax_x.plot(voltage_traces[id][int(timepoints[i-1]):int(timepoints[i])], alpha=0.25, color='white')
        ax_x.spines['right'].set_visible(False)
        ax_x.spines['top'].set_visible(False)
        ax_x.spines['left'].set_visible(False)
        ax_x.spines['bottom'].set_visible(False)
        ax_x.axes.get_xaxis().set_visible(False)
        ax_x.axes.get_yaxis().set_visible(False)
        ax_x.axes.get_xaxis().set_ticks([])
        ax_x.axes.get_yaxis().set_ticks([])
        ax_x.patch.set_alpha(0.0)
        # ani = animation.ArtistAnimation(fig, img, interval=100, blit=True,
        # repeat_delay=1000)
        plt.savefig('movie_' + str(i) + '.png')