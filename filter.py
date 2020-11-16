import McsPy
import McsPy.McsData
from McsPy import ureg, Q_
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, freqz
from IPython import embed
import os


def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def plot_analog_stream_channel(analog_stream, channel_idx, from_in_s=0, to_in_s=None, show=True):
    """
    Plots data from a single AnalogStream channel

    :param analog_stream: A AnalogStream object
    :param channel_idx: A scalar channel index (0 <= channel_idx < # channels in the AnalogStream)
    :param from_in_s: The start timestamp of the plot (0 <= from_in_s < to_in_s). Default: 0
    :param to_in_s: The end timestamp of the plot (from_in_s < to_in_s <= duration). Default: None (= recording duration)
    :param show: If True (default), the plot is directly created. For further plotting, use show=False
    """
    # extract basic information
    ids = [c.channel_id for c in analog_stream.channel_infos.values()]
    channel_id = ids[channel_idx]
    channel_info = analog_stream.channel_infos[channel_id]
    sampling_frequency = channel_info.sampling_frequency.magnitude

    # get start and end index
    from_idx = max(0, int(from_in_s * sampling_frequency))
    if to_in_s is None:
        to_idx = analog_stream.channel_data.shape[1]
    else:
        to_idx = min(analog_stream.channel_data.shape[1], int(to_in_s * sampling_frequency))

    # get the timestamps for each sample
    time = analog_stream.get_channel_sample_timestamps(channel_id, from_idx, to_idx)

    # scale time to seconds:
    scale_factor_for_second = Q_(1, time[1]).to(ureg.s).magnitude
    time_in_sec = time[0] * scale_factor_for_second

    # get the signal
    signal = analog_stream.get_channel_in_range(channel_id, from_idx, to_idx)

    # scale signal to ÂµV:
    scale_factor_for_uV = Q_(1, signal[1]).to(ureg.uV).magnitude
    signal_in_uV = signal[0] * scale_factor_for_uV

    # construct the plot
    _ = plt.figure(figsize=(20, 6))
    _ = plt.plot(time_in_sec, signal_in_uV)
    _ = plt.xlabel('Time (%s)' % ureg.s)
    _ = plt.ylabel('Voltage (%s)' % ureg.uV)
    _ = plt.title('Channel %s' % channel_info.info['Label'])
    if show:
        plt.show()


if __name__ == '__main__':
    mea_file_path = r'D:\Lisa\data\Daniela_h5\2020-05-06T13-58-56Slice2 Test1_BL6 FHM3 P19_coronal_400ms 8psi.h5'

    file = McsPy.McsData.RawData(mea_file_path)
    file_name = os.path.split(file.raw_data_path)[1][:-3]
    file_name = file_name.replace(" ", "_")
    electrode_stream = file.recordings[0].analog_streams[0]
    print(electrode_stream)
    # plot_analog_stream_channel(electrode_stream, 0, from_in_s=0, to_in_s=500)
    # plot_analog_stream_channel(electrode_stream, 9, from_in_s=155, to_in_s=200)
    channel_id = 100
    info = electrode_stream.channel_infos[channel_id].info
    label = info['Label']

    print(label)
    # output of print proves that traces are not filtered
    signal = electrode_stream.get_channel_in_range(channel_id, 0, electrode_stream.channel_data.shape[1])[0]
    Y = np.fft.fft(signal)
    N = int(len(Y)/2 + 1)
    print(N)
    fs = int(electrode_stream.channel_infos[channel_id].sampling_frequency.magnitude)
    dt = 1/fs
    X = np.linspace(0, fs/2, N, endpoint=True)
    print(fs, ', ', dt)
    hann = np.hanning(len(signal))

    Yhann = np.fft.fft(hann*signal)
    # plt.plot(X, 2.0 * np.abs(Yhann[:N]) / N)
    # plt.title('Frequency Domain Signal')
    # plt.xlabel('Frequency ($Hz$)')
    # plt.ylabel('Amplitude ($Unit$)')
    # plt.show()
    lowcut = 100
    highcut = 3000
    b, a = butter_bandpass(lowcut, highcut, fs, order=2)
    w, h = freqz(b, a, worN=2000)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_figheight(9)
    fig.set_figwidth(15)
    ax1.plot(X, 2.0*np.abs(Y[:N])/N, color='#006e7d')
    ax1.set_title('Fourier Analysis')
    ax1.set_xlabel('frequency [Hz]')
    ax1.set_ylabel('Amplitude ($Unit$)')
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ax1.tick_params(labelsize=10, direction='out')
    ax1.grid(True)
    ax2.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = 2", color='#006e7d')
    ax2.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='cutoff', color='#d0797a')
    ax2.set_title('Filter Properties')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Gain')
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.get_xaxis().tick_bottom()
    ax2.get_yaxis().tick_left()
    ax2.tick_params(labelsize=10, direction='out')
    ax2.grid(True)
    ax2.legend(loc='best')
    # fft shows, that there is 50 Hz noise for sure, and the strongest frequency band seems to be around ~350Hz, so I
    # will implement a bandpass filter with cutoffs of 50-500Hz
    # print(signal)
    y = butter_bandpass_filter(signal, lowcut, highcut, fs, order=2)
    time = electrode_stream.get_channel_sample_timestamps(channel_id, 0, None)
    # embed()
    # exit()
    # multiply time with factor 10**-6 to show in s
    ax3.plot(time[0][(100*fs):(101*fs)]*10**-6, signal[(100*fs):(101*fs)], label='unfiltered', alpha=0.5, color='#006e7d', zorder=1)
    ax3.plot(time[0][(100*fs):(101*fs)]*10**-6, y[(100*fs):(101*fs)], label='filtered', alpha=0.75, color='#d0797a', zorder=2)
    ax3.set_title('Unfiltered vs filtered')
    ax3.set_ylabel('amplitude [$\mu$V]')
    ax3.set_xlabel('time [s]')
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.get_xaxis().tick_bottom()
    ax3.get_yaxis().tick_left()
    ax3.tick_params(labelsize=10, direction='out')
    ax3.legend(loc='best')
    plt.savefig(file_name+'_'+label+'_'+str(lowcut)+'_'+str(highcut)+'_middlepart_1s.png')
    plt.show()
