__author__ = 'QHe'

'''
Plot the following relationship for the words in a text file:

log f = log c - s log r

where c and s are constants, r is the ranking of words, and f is the frequency.
'''

from math import log
import make_histogram
import sort_histogram
import simple_plot

def zipf_freq(filename):
    histogram = make_histogram.make_histogram_from_file(filename)
    by_keys, by_values = sort_histogram.sort_histogram(histogram)
    x = []
    y = []
    for f in by_values:
        y.append(log(f[0]))
    for i in range(1, len(by_values)+1):
        x.append(log(i))
    simple_plot.simple_plot(x, y)

if __name__ == '__main__':
    zipf_freq('emma.txt')





