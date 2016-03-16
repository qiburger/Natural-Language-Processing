__author__ = 'Qi_He'

import os, math, operator, sys
from collections import defaultdict, Counter
from nltk.corpus import PlaintextCorpusReader
from nltk import FreqDist, word_tokenize, sent_tokenize

import numpy as np

from subprocess import Popen, PIPE

import pickle

'''
    Toolkit: reusing old tools I built, creating new tools for file and word processing
'''


def get_all_files(directory):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list


def tokenize_sentence(string):
    sent_list = sent_tokenize(string.decode('utf8'))
    return [sent.encode('utf8') for sent in sent_list]


# returns decoded and encoded list of tokenized word in a string
# for this exercise, we do not lowercase all words
def sentence_to_word(string):
    decoded_list = word_tokenize(string.decode('utf8'))
    return [word.encode('utf8') for word in decoded_list]
