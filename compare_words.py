__author__ = 'QHe'

#Compare words in one file against a word bank.

import make_histogram

def compare_words(filename, word_bank):
    histogram = make_histogram.make_histogram_from_file(filename)
    word_bank = make_histogram.make_histogram_from_file(word_bank)
    new_words = []
    for keys in histogram:
        if keys not in word_bank:
            new_words.append(keys)
    return new_words

if __name__ == '__main__':
    print compare_words('pg15237.txt', 'words.txt')