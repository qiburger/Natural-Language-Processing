__author__ = 'QHe'

#Data structure practice based on Think Python Ch. 13

import make_histogram
import random

def choose_from_hist(list):
    selection_list = []
    histogram = make_histogram.make_histogram_from_list(list)
    for keys, values in histogram.items():
        selection_list.extend([keys] * values)
    return random.choice(selection_list)

if __name__ == '__main__':
    print choose_from_hist(make_histogram.make_histogram_from_file('words.txt').keys())
