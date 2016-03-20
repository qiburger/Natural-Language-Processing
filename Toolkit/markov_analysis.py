__author__ = 'QHe'

import random

# global variables
word_map = {}        # map from prefixes to a list of suffixes
prefix = ()          # current tuple of words

def markov_analysis(filename, order=2, n=100, *args):
    global word_map
    global prefix
    for line in open(filename):
        for word in line.rstrip().split():
            t = word.strip().lower()
            if len(prefix) < order:
                prefix += (t,)
                break
            word_map.setdefault(prefix, []).append(t)
            prefix = prefix[1:] + (word,)
    starter = random.choice(word_map.keys())
    print starter
    results = []
    for i in range(n):
        try:
            word = random.choice(word_map[starter])
        except KeyError:
            break
        else:
            results.append(word)
            starter = starter[1:] + (word,)
    return results

if __name__ == '__main__':
    results = markov_analysis('emma.txt', 5, 50)
    print results

