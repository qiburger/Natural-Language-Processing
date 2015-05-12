__author__ = 'QHe'

#Data structure practice based on Think Python Ch. 13

# 13.1
#   Write a program that reads a file, breaks each line into words, strips whitespace and
#   punctuation from the words, and converts them to lowercase.

import string
fin = open("words.txt")
for line in fin:
    word = line.strip().lower()
