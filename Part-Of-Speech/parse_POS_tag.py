
__author__ = 'Qi_He'

import itertools
import os, math, operator, sys
from collections import defaultdict, Counter, OrderedDict
from nltk.corpus import PlaintextCorpusReader
from nltk import FreqDist, word_tokenize, sent_tokenize
import numpy as np
from subprocess import Popen, PIPE
import pickle
import re
from svmutil import *
from nltk.cluster.util import cosine_distance

sample_wsjfile = "/home1/c/cis530/hw3/data/train/wsj_0100.pos"
training_directory = "/home1/c/cis530/hw3/data/train"
testing_directory = "/home1/c/cis530/hw3/data/test"
pos_map_location = "/home1/c/cis530/hw3/data/en-ptb.map"
my_folder = "/mnt/castor/seas_home/h/heqi"
wordtovec = "/home1/c/cis530/hw3/data/w2vec_hw3"


def flatten(listoflists):
    """
    :param listoflists: lists inside a list
    :return: flattened list of lists as a list
    """
    return list(itertools.chain(*listoflists))


def parse_taggedfile(wsjfile, tagmap):
    """
        Part 1: Prepping data
    :param wsjfile: Raw PTB tagged wsjfile
    :param tagmap: PTB to Google Universal

    :return List of [(token, pos)] for each sentence
    """
    sentences_list = []
    sentence_loader = []  # Loads the tag/pos in one sentence

    with open(wsjfile, "r") as tagged_file:
        for line in tagged_file:
            if line.startswith("======"):  # Ignore "==" line as instructed
                pass
            elif line.strip() == "":
                if len(sentence_loader) > 0:
                    sentences_list.append(sentence_loader)
                sentence_loader = []
            else:
                line = line.replace("]", "").strip(" [")  # I was having issue stripping "]"
                sentence_loader.extend(parse_tagged_line(line.split(), tagmap))
        if len(sentence_loader) > 0:
            sentences_list.append(sentence_loader)
    return sentences_list


def parse_tagged_line(line, tagmap):
    """

    :param line: [token/PTB POS] from each line of the file
    :param tagmap: PTB to Google Universal
    :return [(token, Google POS)]
    """
    output_list = []
    for pairs in line:
        pairs_list = pairs.split("/")
        if not tagmap:
            google_tag = tagmap.setdefault(pairs_list[1], pairs_list[1])  # return PTB tag if the map is N/A
        else:
            google_tag = tagmap.setdefault(pairs_list[1], "NOUN")  # return "NOUN" if the map is N/A
        output_list.append((pairs_list[0].lower(), google_tag))
    return output_list