import h5py
import scipy.signal
from scipy.signal import savgol_filter
import matplotlib
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
from IPython import embed
# use agg backend due to performance issues
matplotlib.use("agg")


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
                v_k.append(float(columns[2]) * 1000000)
                v_dc.append(float(columns[4]) * 1000000)
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
    if columns[0] > ord('P'):
        columns[0] -= 2
    if columns[1] > ord('P'):
        columns[1] -= 2

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

# using the savgol filter instead
# def butter_filter(cutoff, fs, mode, order=2):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff/nyq
#     b, a = butter(order, normal_cutoff, btype=mode, analog=False)
#     return b, a
#
#
# def butter_div_filters(data, cutoff_freq, fs, mode):
#     # as far as I understood it, all three filter types (low, high, notch) can be applied with these functions
#     # and which filter will be applied at the end depends on the chosen mode
#     b, a = butter_filter(cutoff_freq, fs, mode)
#     y = filtfilt(b, a, data)
#     return y


mea_recording_path = "/home/lisa_ruth/mea_recordings/second_movie" \
                     "/2020-08-26T14-49-54FHM3_GS967_BL6_P19_male_400ms_7psi_Slice3_Test1_WITH.h5"
electrode_asciis = "/home/lisa_ruth/mea_recordings/second_movie/Lisa ASCII/200826/" \
                   "/FHM3_GS967_BL6_P19_male_400ms_7psi_Slice3_Test1_WITH_Sweep1.txt"
video_path = "/home/lisa_ruth/mea_recordings/second_movie" \
             "/FHM3_GS967_BL6_P19_male_exp100ms_dur100sec_400ms_7psi_Slice3_Test1_WITH_4movie.tif"

mea_file = h5py.File(mea_recording_path, 'r')
mats = tiff.imread(video_path)

relevant_labels = ['F4', 'F5', 'F6', 'F7', 'F8', 'G4', 'G5', 'G6', 'G7', 'G8', 'H4', 'H5', 'H6', 'H7', 'H8', 'J4', 'J5',
                   'J6', 'J7', 'J8', 'K4', 'K5', 'K6', 'K7', 'K8', 'L4', 'L5', 'L6', 'L7', 'L8', 'M4', 'M5', 'M6', 'M7',
                   'M8', 'N4', 'N5', 'N6', 'N7', 'N8', 'O4', 'O5', 'O6', 'O7', 'O8', 'R4', 'R5', 'R6', 'R7', 'R8']
label = 'F4'

x0, y0 = (0.15, 0.76)
x_offset, y_offset = (0.06725, -0.089)
plot_positions = calculate_plot_positions(label, x0, y0, x_offset, y_offset, relevant_labels)

electrode_indices, time_electrode, v_k, v_dc = read_ascii_file(electrode_asciis)
filtered_vk = savgol_filter(v_k, window_length=1001, polyorder=3, deriv=0, delta=5e-5)
filtered_vdc = savgol_filter(v_dc, window_length=1001, polyorder=3, deriv=0, delta=5e-5)

stepsize = 1000
num_frames = len(mats)
voltage_traces = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['ChannelData'][:]
timepoints = np.arange(stepsize, (num_frames * stepsize) + 1, stepsize)
sampling_rate = 10000
conversion_factor = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['ConversionFactor']
exponent = mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'][0]['Exponent'] + 6 #6 = pV -> uV
channels_voltage_traces = []
for i, label in enumerate(relevant_labels):
    id = get_channel_id(label)
    #  mea_file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel']
    voltage_trace_snippet = (voltage_traces[id][:int(stepsize * num_frames)]).astype(float)
    scaled_snippet = voltage_trace_snippet * conversion_factor * np.power(10.0, exponent)
    channels_voltage_traces.append(scaled_snippet)

ylim_0 = np.percentile(channels_voltage_traces, 0.05)
ylim_1 = np.percentile(channels_voltage_traces, 99.95)

for i, mat in enumerate(mats):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    line = plt.imshow(mat, cmap='gray', interpolation='none')
    # fig.text(0.801, 0.651, '*', size=24, ha='center', va='center', color='#6301e5')
    fig.text(0.801, 0.651, '*', size=24, ha='center', va='center', color='#00c4e0')
    fig.text(0.7625, 0.545, '*', size=24, ha='center', va='center', color='#6301e5')
    plt.axis('off')

    matplotlib.rc('axes', edgecolor='#6301e5')
    # ax_k = fig.add_axes([0.35, 0.3, 0.5, 0.05])
    ax_dc = fig.add_axes([0.35, 0.3, 0.5, 0.05])

    matplotlib.rc('axes', edgecolor='#00c4e0')
    # ax_dc = fig.add_axes([0.35, 0.2, 0.5, 0.05])
    ax_k = fig.add_axes([0.35, 0.2, 0.5, 0.05])

    color = 'gray'
    alpha = 0.5

    for j, label in enumerate(plot_positions.keys()):
        position = plot_positions[label]
        ax_x = fig.add_axes([position[0], position[1], 0.05, 0.05])
        f, t, Sxx = scipy.signal.spectrogram(channels_voltage_traces[j], sampling_rate, nperseg=2 ** 9, noverlap=2 ** 8)

        if i == 0:
            plot_snippet = channels_voltage_traces[j][:int(timepoints[i])]
            ax_x.plot(plot_snippet, alpha=alpha, color=color)
            ax_x.text(position[0], position[1], label, color=color, fontsize=8)
        if j == 4:
            matplotlib.rc('axes', edgecolor='gray')
            ax_scale = fig.add_axes([position[0] + 0.05, position[1] + (y_offset - 0.05), 0.05, 0.05])
            ax_scale.spines['right'].set_visible(False)
            ax_scale.spines['top'].set_visible(False)
            ax_scale.set_ylim(ylim_0, ylim_1)
            ax_scale.set_xlim(0, 1000)
            ax_scale.axes.get_xaxis().set_ticks([])
            ax_scale.axes.get_yaxis().set_ticks([])
            ax_scale.set_ylabel(r'%i $\mu$V' % (ylim_1 - ylim_0))
            ax_scale.set_xlabel('100 msecs')
            ax_scale.tick_params(axis='x', colors='gray')
            ax_scale.tick_params(axis='y', colors='#6301e5')
            ax_scale.yaxis.label.set_color('gray')
            ax_scale.xaxis.label.set_color('gray')
            ax_scale.patch.set_alpha(0.0)
        plot_snippet = channels_voltage_traces[j][int(timepoints[i - 1]):int(timepoints[i])]
        if i > 2:
            relevant_freq_found = False
            for fi, freq in enumerate(f):
                if np.abs(freq - 20) <= 1:

                    if np.max(Sxx[fi][((int(timepoints[i - 1]) / sampling_rate) < t) &
                                      (t <= (int(timepoints[i]) / sampling_rate))]) >= 5:
                        relevant_freq_found = True
                        break
            if relevant_freq_found:
                color = '#006d7c'
                alpha = 0.5
            else:
                color = 'gray'
                alpha = 0.5
        ax_x.plot(plot_snippet, alpha=alpha, color=color)
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

    mv_factor = 1000
    ax_k.plot(filtered_vk[:int(timepoints[i] * 2)]/mv_factor, color='#6301e5')
    ax_k.set_ylim((np.min(filtered_vk) - 100)/mv_factor, (np.max(filtered_vk) + 100)/mv_factor)
    ax_k.set_xlim(0, (num_frames * stepsize) * 2)
    ax_k.set_xlabel('time [s]')
    ax_k.set_ylabel('V [mV]', loc='top')
    ax_k.set_xticklabels(np.arange(0, (num_frames * stepsize) / sampling_rate, 10))
    ax_k.spines['right'].set_visible(False)
    ax_k.spines['top'].set_visible(False)
    ax_k.spines['bottom'].set_color('#6301e5')
    ax_k.spines['left'].set_color('#6301e5')
    ax_k.tick_params(axis='x', colors='#6301e5')
    ax_k.tick_params(axis='y', colors='#6301e5')
    ax_k.yaxis.label.set_color('#6301e5')
    ax_k.xaxis.label.set_color('#6301e5')
    ax_k.patch.set_alpha(0.0)

    ax_dc.plot((filtered_vdc[:int(timepoints[i] * 2)])/mv_factor, color='#00c4e0')
    ax_dc.set_xlabel('time [s]')
    ax_dc.set_ylabel('V [mV]', loc='top')
    ax_dc.set_ylim((np.min(filtered_vdc) - 100)/mv_factor, (np.max(filtered_vdc) + 100)/mv_factor)
    ax_dc.set_xlim(0, (num_frames * stepsize) * 2)
    ax_dc.set_xticklabels(np.arange(0, (num_frames * stepsize) / sampling_rate, 10))
    ax_dc.tick_params(axis='x', colors='#00c4e0')
    ax_dc.tick_params(axis='y', colors='#00c4e0')
    ax_dc.spines['right'].set_visible(False)
    ax_dc.spines['top'].set_visible(False)
    ax_dc.spines['bottom'].set_color('#00c4e0')
    ax_dc.spines['left'].set_color('#00c4e0')
    ax_dc.yaxis.label.set_color('#00c4e0')
    ax_dc.xaxis.label.set_color('#00c4e0')
    ax_dc.patch.set_alpha(0.0)
    # plt.show()
    # if i == 5:
    #     embed()
    plt.savefig('0_movie_200826_movie' + str(i) + '.png')
    print('figure', i, 'saved')
