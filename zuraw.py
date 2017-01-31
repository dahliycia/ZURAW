import os
import wave
# scipy and numpy for Windows from http://www.lfd.uci.edu/~gohlke/pythonlibs/
from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import scipy.signal


def normalize_data(data, sampFreq):
    new_data = []
    if len(data) != size(data):
        data = data[:, 0]
    if data.dtype == 'uint8':
        new_data = data - 128
        # for i in data:
        #     new_data.append(i-128)
    else:
        new_data = data
    new_data = butter_highpass_filter(new_data, 30, 11025)
    data_max = max(abs(new_data))
    new_data_temp = []
    for i in new_data:
        new_data_temp.append(float(i)/float(data_max))

    dev = sampFreq/11025
    if dev == 0:
        dev = 1
    new_data2 = new_data_temp[::dev]
    # new_data4 = lowpass_filter(new_data3, 20000, 11025)
    return new_data2

def lowpass_filter(data, cutoff, fs):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b,a = scipy.signal.butter(1, normal_cutoff, btype='low')
    y = scipy.signal.filtfilt(b, a, data)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = scipy.signal.filtfilt(b, a, data)
    return y


def get_fourier(ex, n, sampFreq):
    fourier = fft(ex, norm="ortho")
    if len(fourier) %2 > 0:
        mid = (len(fourier) + 1)/2
    else:
        mid = len(fourier)/2

    fourier = abs(fourier[0:mid])
    fourier = fourier**2
    cut = max(fourier)/20
    cut_point = 0
    for i in range(0, len(fourier)):
        if fourier[i] > cut:
            cut_point = i

    fourier = fourier[0:cut_point]

    fourier = fourier/float(max(fourier))

    scale = int(len(fourier)/100)
    new_fourier = []
    for i in range(0, len(fourier), scale):
        temp = sum(fourier[i:i+scale])/scale
        new_fourier.append(temp)

    # print len(new_fourier)
    #
    # plt.plot(new_fourier)
    # plt.show()
    return new_fourier


def get_example(example, type_path):
    if example.endswith('.wav'):
        example_path = type_path + example
        sampFreq, ex = wavfile.read(example_path)
        ex = normalize_data(ex, sampFreq)
        n = len(ex)
        ex_fourier = get_fourier(ex, n, sampFreq)
        ex_dict = {'ex': ex, 'ex_fourier': ex_fourier}
        return ex_dict


def get_pattern(type_dict):
    temp_pattern = []
    cnt = 0
    for example in type_dict['examples']:
        if example:
            for i in range(0, len(example['ex_fourier'])):
                if i < len(temp_pattern):
                    temp_pattern[i] += example['ex_fourier'][i]
                else:
                    temp_pattern.append(example['ex_fourier'][i])
            cnt +=1
    # print 'temp pattern length: ' + str(len(temp_pattern))
    pattern = []
    for i in temp_pattern:
        pattern.append(i/float(cnt))
    # plt.plot(pattern)
    # plt.show()
    save_pattern(pattern, type_dict['name'], 'patterns/')
    return pattern


def save_pattern(pattern, name, pattern_path):
    pattern_file = open(pattern_path + name + '.txt', 'w')
    for i in pattern:
        pattern_file.write(str(i) + '\n')
    pattern_file.close()


def find_types():
    data_path = 'data/'
    types_list = []
    for type_name in os.listdir(data_path):
        type_dict = {'name': type_name, 'examples': []}
        type_path = data_path + type_name + '/'
        for example in os.listdir(type_path):
            ex_dict = get_example(example, type_path)
            type_dict['examples'].append(ex_dict)
        type_dict['pattern'] = get_pattern(type_dict)
        types_list.append(type_dict)
    return types_list


def main():
    types_list = find_types()


if __name__ == '__main__':
    main()
