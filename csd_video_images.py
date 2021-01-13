import h5py
import matplotlib
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
import time
# use agg backend due to performance issues
matplotlib.use("agg")
from IPython import embed


def read_ascii_file(file):
    f = open(file, 'r')
    indices = []
    time = []
    v_k = []
    v_dc = []
    for k, line in enumerate(f):
        line = line.strip()
        columns = line.split(', ')

        if 3 <= k < 2000004 and len(columns) > 1:
            try:
                indices.append(float(columns[0]))
                time.append(float(columns[1]))
                v_k.append(float(columns[2]))
                v_dc.append(float(columns[4]))
            except ValueError:
                embed()
    return np.array(indices), np.array(time), np.array(v_k), np.array(v_dc)


def get_distance(label_a, label_b):
    '''''
    This function gets the two labels of the channels which voltage traces are going to be plotted to calculate the 
    distance between these two consecutive subplots.
    input: strings of the respective channel labels
    returns: col_diff and rof_diff which are the distances of the subplots
    '''''
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
    '''''
    This function calculates the exact position of the respective subplots
    input:
        reference_label: the label of the channel, which is seen in the upper left corner of the video
        x0: x position of the subplot of the channel in the upper left corner
        y0: y position of the the subplot of the channel in the upper left corner
        x_offset: distance between each row
        y_offset: distance between each column
        relevant_labels: strings of all channels seen on the video which should be plotted
    return:
        positions: x- and y-coordinate of the resulting subplots
    '''''
    positions = dict()

    for label in relevant_labels:
        col_diff, row_diff = get_distance(reference_label, label)
        positions[label] = (x0 + col_diff * x_offset, y0 + row_diff * y_offset)

    return positions


def get_channel_id(label):
    for ch in mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']:
        if label == ch[4].decode('utf8'):
            return ch[1]


mea_recording_path = "/home/lisa_ruth/mea_recordings/CSD_data/h5_data" \
                     "/2020-10-13T14-27-38FHM3_GS967_BL6_P15_male_400ms_7psi_Slice3_Test1_WITH.h5"
electrode_asciis = "/home/lisa_ruth/mea_recordings/FHM3_GS967_BL6_P15_male_400ms_7psi_Slice3_Test1_WITH.txt"
video_path = "/home/lisa_ruth/mea_recordings/CSD_data/201013_microscope" \
             "/FHM3_GS967_BL6_P15_male_exp100ms_dur100sec_400ms_7psi_Slice2_Test3_4movie.tif"


mea_file = h5py.File(mea_recording_path, 'r')
mats = tiff.imread(video_path)

relevant_labels = ['C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'E3', 'E4',
                   'E5', 'E6', 'E7', 'E8', 'E9', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G3', 'G4', 'G5', 'G6',
                   'G7', 'G8', 'G9', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9',
                   'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'M3', 'M4', 'M5',
                   'M6', 'M7', 'M8', 'M9', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9']
label = 'C3'
x0, y0 = (0.185, 0.7125)
x_offset, y_offset = (0.06, -0.09)
plot_positions = calculate_plot_positions(label, x0, y0, x_offset, y_offset, relevant_labels)

electrode_indices, time_electrode, v_k, v_dc = read_ascii_file(electrode_asciis)

stepsize = 1000
num_frames = len(mats)
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
# [:int(stepsize*num_frames)]
timepoints = np.arange(stepsize, (num_frames * stepsize) + 1, stepsize)
channels_voltage_traces = []
for i, label in enumerate(relevant_labels):
    id = get_channel_id(label)
    voltage_trace_snippet = voltage_traces[id][:int(stepsize*num_frames)]
    channels_voltage_traces.append(voltage_trace_snippet)
ylim_0 = np.percentile(channels_voltage_traces, 2.5) - 1526.5
ylim_1 = np.percentile(channels_voltage_traces, 97.5) + 1526.5
for i, mat in enumerate(mats):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    plt.imshow(mat, cmap='gray', interpolation='none')
    plt.axis('off')
    for j, label in enumerate(plot_positions.keys()):
        position = plot_positions[label]
        ax_x = fig.add_axes([position[0], position[1], 0.05, 0.05])
        ax_k = fig.add_axes([0.6525, 0.665, 0.05, 0.05])
        ax_dc = fig.add_axes([0.6525, 0.5775, 0.05, 0.05])
        if i == 0:
            ax_x.plot(channels_voltage_traces[j][:int(timepoints[i])], alpha=0.25, color='white')
            ax_x.text(position[0], position[1], label, color='white', fontsize=8)
            ax_k.plot(time_electrode[:2*stepsize], v_k[:2*stepsize], color='#6301e5')
            ax_dc.plot(time_electrode[:2*stepsize], v_dc[:2*stepsize], color='#00c4e0')
        if j == 6:
            matplotlib.rc('axes', edgecolor='white')
            ax_scale = fig.add_axes([position[0]+0.00825, position[1]+(y_offset+0.055), 0.05, 0.05])
            ax_scale.spines['right'].set_visible(False)
            ax_scale.spines['top'].set_visible(False)
            ax_scale.set_ylim(ylim_0, ylim_1)
            ax_scale.set_xlim(0, 1000)
            ax_scale.axes.get_xaxis().set_ticks([])
            ax_scale.axes.get_yaxis().set_ticks([])
            ax_scale.set_ylabel(r'%i $\mu$V' % (ylim_1-ylim_0))
            ax_scale.set_xlabel('100 msecs')
            ax_scale.yaxis.label.set_color('white')
            ax_scale.xaxis.label.set_color('white')
            ax_scale.patch.set_alpha(0.0)
        ax_x.plot(channels_voltage_traces[j][int(timepoints[i - 1]):int(timepoints[i])], alpha=0.25, color='white')
        ax_x.set_ylim(ylim_0, ylim_1)
        ax_x.spines['right'].set_visible(False)
        ax_x.spines['top'].set_visible(False)
        ax_x.spines['left'].set_visible(False)
        ax_x.spines['bottom'].set_visible(False)
        ax_x.axes.get_xaxis().set_visible(False)
        ax_x.axes.get_yaxis().set_visible(False)
        ax_x.axes.get_xaxis().set_ticks([])
        ax_x.axes.get_yaxis().set_ticks([])
        ax_x.patch.set_alpha(0.0)
        ax_k.plot(time_electrode[int(timepoints[i - 2]):int(timepoints[i+1])],
                  v_k[int(timepoints[i - 2]):int(timepoints[i + 1])], color='#6301e5')
        ax_k.set_ylim(ylim_0, ylim_1)
        ax_k.spines['right'].set_visible(False)
        ax_k.spines['top'].set_visible(False)
        ax_k.spines['left'].set_visible(False)
        ax_k.spines['bottom'].set_visible(False)
        ax_k.axes.get_xaxis().set_visible(False)
        ax_k.axes.get_yaxis().set_visible(False)
        ax_k.axes.get_xaxis().set_ticks([])
        ax_k.axes.get_yaxis().set_ticks([])
        ax_k.patch.set_alpha(0.0)
        ax_dc.plot(time_electrode[int(timepoints[i - 2]):int(timepoints[i+1])],
                   v_dc[int(timepoints[i - 2]):int(timepoints[i + 1])], color='#00c4e0')
        ax_dc.set_ylim(ylim_0, ylim_1)
        ax_dc.spines['right'].set_visible(False)
        ax_dc.spines['top'].set_visible(False)
        ax_dc.spines['left'].set_visible(False)
        ax_dc.spines['bottom'].set_visible(False)
        ax_dc.axes.get_xaxis().set_visible(False)
        ax_dc.axes.get_yaxis().set_visible(False)
        ax_dc.axes.get_xaxis().set_ticks([])
        ax_dc.axes.get_yaxis().set_ticks([])
        ax_dc.patch.set_alpha(0.0)
    plt.savefig('movie_a_' + str(i) + '.png')
    print('figure', i, 'saved')

