# ZURAW
Python Sound Pattern Recognition System

## What is ZURAW
ZURAW is a small project which recognizes (to it's best) sounds using previously created patterns. It means it is first learning, then recognizing.
The ZURAW project consists of two programs which are run separately, but are dependant on each other:
- _zuraw.py_ - the learning program. It goes through each file from the _data/_ directory, and creates a pattern for each category (see more about how to add your data below)
- _zuraw_recognize.py_ - the recognizing program, which takes your input file, processes it and matches to a computed pattern.

##Requirements
- python 2.7 or higher
- scipy (needs numpy)
- pylab
- your sound files in .wav

For Windows, you can install scipy and numpy from http://www.lfd.uci.edu/~gohlke/pythonlibs/

For Linux, go with `pip install numpy` and `pip install scipy`

##How to use

ZURAW is easy to use. It takes general two steps to use it properly:

###1. Learn the patterns

ZURAW needs to learn from examples before it can recognize sounds for you. All your examples should be added in the _data/_ directory under separate directories for each category.

For ex.:
- data/DOG/dog1.wav
- data/DOG/dog2.wav
- data/CAT/cat1.wav

etc. There are some files already in the repo's _data/_ directory, you can look there for reference and delete them if not needed.

When you have already added your patterns, simply run `python zuraw.py`. It will create pattern files in the _patterns/_ directory. It may take a few minutes to run.

###2. Recognize your example
ZURAW by default recognizes all examples found in _test/_ directory. 

Add your files to _test/_ directory, for ex.: _test/ex1.wav_, _test/ex.2wav_.

Then run `python zuraw_recognize.py` and it will inform you how the files were recognized.


## What you can implement with it

__Q: I would like to use some methods from ZURAW in my project. What methods can I use? How?__

### zuraw.py methods 

- __find_types()__ - goes though the _data/_ directory and produces patterns under _patterns/_ directory. This is the main function which calls other functions to do all the computing work.
  * returns: dictionary with all patterns and examples data

- __save_pattern(pattern, name, pattern_path)__ - saves \*pattern\* in \*pattern_path\*/\*name\*.txt file.

- __get_pattern(type_dict)__ - creates a pattern for one type(category) from examples in the \*type_dict\*.
  * returns: pattern (array of float) - pattern is a mean of filtered fourier transforms of your examples

- __get_example(example_name, type_path)__ - for a single \*example_name\* it reads the .wav file and computes data.
  * returns: ex_dict - a dictionary with 'ex': normalized example data, 'ex_fourier': computed filtered fft

- __get_fourier(example, ex\_length, sampFreq)__ - for a normalized \*example\* computes the filtered fourier transform
  * returns: new_fourier - filtered fourier transform array

- __normalize_data(data, sampFreq)__ - normalizes different types of input data
  * returns: new_data - normalized data array

### zuraw_recognize.py methods

- __main(file_name, file_path)__ - recognizes \*file_path\*\\*file_name\* comparing to patterns in _patterns/_

- __load_patterns(patterns_dir)__ - loads pattern files from \*patterns_dir\*
  * returns: patterns_dict - a dictionary of patterns under their names

- __recognize(my_dict, patterns_dict)__ - recognizes a single file
*IMPORTANT* You need to compute my_dict with *zuraw.get_example(file_name, file_path)*

- __measure_similarity(item, pattern)__ - measures similarity between the \*item\* and a single \*pattern\*

## How it works

In this section you can find how (technically) the most important modules work.
