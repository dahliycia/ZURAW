import os
import wave
# scipy and numpy for Windows from http://www.lfd.uci.edu/~gohlke/pythonlibs/
from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import scipy.signal


def normalize_data(data):
    new_data = []
    if data.dtype == 'uint8':
        for i in data:
            new_data.append(i-128)
    else:
        new_data = data
    return new_data


def get_fourier(ex, n, sampFreq):
    fourier = fft(ex)
    if len(fourier) %2 > 0:
        mid = (len(fourier) + 1)/2
    else:
        mid = len(fourier)/2
    fourier = abs(fourier[0:mid])

    plt.plot(fourier)
    plt.show()
    return fourier


def get_example(example, type_path):
    if example.endswith('.wav'):
        example_path = type_path + example
        sampFreq, ex = wavfile.read(example_path)
        ex = normalize_data(ex)
        n = len(ex)
        ex_fourier = get_fourier(ex, n, sampFreq)
        ex_dict = {'ex': ex, 'ex_fourier': ex_fourier}
        return ex_dict


def find_types():
    data_path = 'data/'
    types_list = []
    for type_name in os.listdir(data_path):
        type_dict = {'name': type_name, 'examples': []}
        type_path = data_path + type_name + '/'
        for example in os.listdir(type_path):
            ex_dict = get_example(example, type_path)
            type_dict['examples'].append(ex_dict)
        types_list.append(type_dict)
    print types_list


def main():
    get_example('dog_bark3.wav', 'data/dog/')
    get_example('dog_bark2.wav', 'data/dog/')
    get_example('dog_bark4.wav', 'data/dog/')



if __name__ == '__main__':
    main()