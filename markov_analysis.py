__author__ = 'QHe'

# global variables
word_map = {}        # map from prefixes to a list of suffixes
prefix = ()            # current tuple of words

def markov_analysis(filename, n):
    global word_map
    word_list = []
    for line in open(filename):
        for word in line.rstrip().split():
            t = word.strip().lower()
            word_list.append(t)
    for i in range(len(word_list)-n):
        key = word_list[i]
        word_map.setdefault(key,[]).append(word_list[i+n])
    return word_map

if __name__ == '__main__':
    word_bank = markov_analysis("pg15237.txt", 1)
    print word_bank

