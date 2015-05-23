__author__ = 'QHe'

'''
Plot the following relationship for the words in a text file:

log f = log c - s log r

where c and s are constants, r is the ranking of words, and f is the frequency.
'''
import math
import make_histogram
import sort_histogram
import simple_plot

def zipf_freq(filename):
    histogram = make_histogram.make_histogram_from_file(filename)
    by_keys, by_values = sort_histogram.sort_histogram(histogram)
    for i in by_values:
        x = math.log(i)
        x +






