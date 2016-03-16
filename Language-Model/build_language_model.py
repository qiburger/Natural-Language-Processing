import os, math, operator, sys
from collections import defaultdict, Counter
from nltk.corpus import PlaintextCorpusReader
from nltk import FreqDist, word_tokenize, sent_tokenize

import numpy as np

from subprocess import Popen, PIPE

import pickle
from toolkit import *



"""
    Building a language model
    - train a bigram language model using all of the training data in data/train.
    - The model handle out-of-vocabulary words and use add 0.25 smoothing

"""

class BigramModel:

    lang_model = []
    token_list = []
    bigram_dict = defaultdict(lambda: 0.0)
    words_dict = defaultdict(lambda: 0.0)

    # 1. constructor
    def init(self, trainfiles):
        """
        builds a bigram language model from the text found in a list of plain text files specified in trainfiles.
        :param trainfiles: list of filenames, given with absolute paths.
        """
        for filepaths in trainfiles:

            # load files and tokenize words in sentences
            with open(filepaths, "r") as text:
                sent_list = tokenize_sentence(text.read())

                for sentences in sent_list:
                    word_list = sentence_to_word(sentences)

                    # check unknown words
                    for index, words in enumerate(word_list):
                        if words not in self.token_list:
                            word_list[index] = "<UNK>"

                            # add word to vocab
                            self.token_list.append(words)

                    word_list.insert(0, "<s>")
                    word_list.append("</s>")

                    for i in range(len(word_list)-1):
                        self.lang_model.append((word_list[i], word_list[i+1]))

        for (word1, word2) in self.lang_model:
            self.bigram_dict[(word1, word2)] += 1
            self.words_dict[word1] += 1

    def logprob(self, prior_context, target_word):
        """
        returns the base-2 log probability of the given word (target word) given a specific context (prior context).
        :param prior_context: str
        :param target_word: str
        :return: float log-probability of the target word to occur after the prior context.
        """

        # dealing with unseen words
        if prior_context not in self.words_dict:
            prior_context = "<UNK>"
        if target_word not in self.words_dict:
            target_word = "<UNK>"

        # for unseen combinations: default dicts have default value of 0.0
        bigram_count = self.bigram_dict[(prior_context, target_word)]
        context_count = self.words_dict[prior_context]


        # add 0.25 smoothing for out-of-vocabulary words
        prob = (bigram_count + 0.25) / (context_count + 0.25 * len(self.token_list))

        return np.log(prob) / np.log(2)
