__author__ = 'QHe'

import make_histogram
import random
import bisect

#Choose from a list constructed based on cumulative distribution of words
#Input - histogram (dictionary), output - the randomly chosen word (string)
def choose_from_hist(hist):
    selection_list = []
    for keys, values in hist.items():
        selection_list.extend([keys] * values)
    return random.choice(selection_list)

#Choose a random word by constructing a cumulative distribution list of words
#Input - histogram (dictionary), output - the randomly chosen word (string)
def choose_from_cdf(hist):
    word_list = hist.keys()
    cdf = []
    counter = 0
    for keys in hist:
        counter += hist[keys]
        cdf.append(counter)
    random_number = random.randint(0, counter-1)
    index = bisect.bisect(cdf, random_number)
    return word_list[index]

if __name__ == '__main__':
    print choose_from_hist(make_histogram.make_histogram_from_file('words.txt'))
    print choose_from_cdf(make_histogram.make_histogram_from_file('words.txt'))