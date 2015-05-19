__author__ = 'QHe'

#Data structure practice based on Think Python Ch. 13

# 13.1
#   Write a program that reads a file, breaks each line into words, strips whitespace and
#   punctuation from the words, and converts them to lowercase.
#   Returns a dictionary of words, and the total number of words.

import make_histogram
import sort_histogram

if __name__ == '__main__':
    histogram = make_histogram.make_histogram("pg15237.txt")
    word_count = sum(histogram.values())
    temp, histogram_sorted = sort_histogram.sort_histogram(histogram)







