import zuraw
import os

def load_patterns(patterns_path):
    patterns_dict = {}
    for pattern_file_name in os.listdir(patterns_path):
        if pattern_file_name.endswith('.txt'):
            pattern_dir = patterns_path + '/' + pattern_file_name
            pattern_file = open(pattern_dir, 'r')
            pattern_list = pattern_file.readlines()
            pattern = []
            for i in pattern_list:
                pattern.append(float(i))
            patterns_dict[pattern_file_name[0:-3]] = pattern
    return patterns_dict


def measure_similarity(item, pattern):
    # mean squared error
    err = 0
    length = min(len(pattern), len(item))
    for i in range(0, length):
        err += abs(pattern[i]-item[i])**2

    err = err/len(item)
    return err


def recognize(my_dict, patterns_dict):
    current_smallest_err = 1
    current_name = 'not_recognized'
    for name, pattern in patterns_dict.items():
        err = measure_similarity(my_dict['ex_fourier'], pattern)
        # print err
        if err < current_smallest_err:
            current_smallest_err = err
            current_name = name
    print 'recognized as: ' + current_name



def main(file_name, file_path):
    my_dict = zuraw.get_example(file_name, file_path)
    patterns_dict = load_patterns('patterns/')
    recognize(my_dict, patterns_dict)



if __name__ == '__main__':
    for test in os.listdir('test/'):
        print test
        main(test, 'test/')
