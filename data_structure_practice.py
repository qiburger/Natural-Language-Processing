__author__ = 'QHe'

#Data structure practice based on Think Python Ch. 13

# 13.1
#   Write a program that reads a file, breaks each line into words, strips whitespace and
#   punctuation from the words, and converts them to lowercase.
#   Returns a dictionary of words, and the total number of words.

import string
import collections

def collect_words(filename):
    word_dict = collections.defaultdict(int)
    word_counter = 0
    for line in open(filename):
        line = line.replace('-', ' ')
        for word in line.split():
            word_counter += 1
            t = word.strip(string.punctuation + string.whitespace).lower()
            word_dict[t] += 1
    return (word_dict, word_counter)

word_dict, word_counter = collect_words("pg15237.txt")


