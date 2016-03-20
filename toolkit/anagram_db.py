__author__ = 'QHe'

import anagram
import shelve
import pickle

def store_anagrams(filename):
    shelf = shelve.open(filename, 'c')
    anagram_map = anagram.get_anagrams('words.txt')
    for words, anagrams in anagram_map.iteritems():
        shelf[words] = anagrams
    shelf.close()

def read_anagrams(word):
    try:
        db = shelve.open('anagram.db')
        word = ''.join(sorted(list(word)))
        return db[word]
    except:
        print 'db n/a or word is not included in the map'

if __name__ == '__main__':
    store_anagrams('anagram.db')
    print read_anagrams('static')