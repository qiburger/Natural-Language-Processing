
__author__ = 'Qi_He'

import itertools


import os, math, operator, sys
from collections import defaultdict, Counter, OrderedDict
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import wordnet as wn
from nltk import FreqDist, word_tokenize, sent_tokenize
import numpy as np
from subprocess import Popen, PIPE
import pickle
import re
from nltk.cluster.util import cosine_distance

'''
    File directories
'''

dev_input = "/home1/c/cis530/hw4/dev_input"
dev_10 = "/home1/c/cis530/hw4/dev_input/dev_10"
dev_10_example = "/home1/c/cis530/hw4/dev_input/dev_10/APW19981025.0234"

dev_model = "/home1/c/cis530/hw4/dev_models"
topic_word_tool = "/home1/c/cis530/hw4/TopicWords-v2/"
topic_command = "java -Xmx1000m TopicSignatures "
topic_address = "//home1//h//heqi//cis530//hw4//config"

input_dir_string = "inputDir = /home1/c/cis530/hw4/dev_input/"
output_file_string = "outputFile = /home1/h/heqi/cis530//hw4/config/"
lex_parser_addr = "/home1/c/cis530/hw4/lexparser.sh"


'''
    Batch generator

    The folder /home1/c/cis530/hw4/dev input contains 40 subdirectories (clusters) of documents.
    Each cluster contains 10 news articles covering the same event or topic.
    We will run the TopicWords tool for each cluster.
'''


def make_config_files():
    single_digit_name = "dev_0"
    double_digit_name = "dev_"
    config_name = "./config/config."
    with open("./config/config.example", "r") as example:
        listout = [line.rstrip() for line in example]
        for i in range(40):
            if i < 10:
                temp_name = single_digit_name + str(i)
            else:
                temp_name = double_digit_name + str(i)
            temp_out = config_name + str(i)
            with open(temp_out, "w") as fout:
                for counter in range(len(listout)):
                    if counter == 8:
                        fout.write((listout[counter] + temp_name + '\n'))
                    elif counter == 12:
                        fout.write((listout[counter] + temp_name + '.ts\n'))
                    else:
                        fout.write(listout[counter] + '\n')


def make_ts_files():
    for i in range(40):
        temp_command = topic_command + topic_address + "//config." + str(i)
        Popen(temp_command, cwd=r"/home1/c/cis530/hw4/TopicWords-v2", shell=True)


def load_topic_words(topic_file, n):
    """
    Given a .ts file and integer n, returns a list of the top-n topic words from that file
    in order of descending X2 statistic.
    :param topic_file: str path
    :param n: int
    :return: list of str length n
    """
    topic_words_dict = {}
    with open(topic_file, "r") as f:
        for line in f:
            temp_line = line.split()
            stat = float(temp_line[1])
            if stat >= 10:
                topic_words_dict[temp_line[0]] = stat
    sorted_tuple = sorted(topic_words_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return [tuples[0] for tuples in sorted_tuple][:(min(n, len(sorted_tuple)))]

