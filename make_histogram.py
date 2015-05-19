__author__ = 'QHe'

#The function returns a histogram of words in text file
#The function reads a file, breaks each line into words, strips whitespace and
# punctuation from the words, and converts them to lowercase.

import collections
import string

def make_histogram(filename):
    histogram = collections.defaultdict(int)
    for line in open(filename):
        line = line.replace('-', ' ')
        for word in line.split():
            t = word.strip(string.punctuation + string.whitespace).lower()
            histogram[t] += 1
    return histogram