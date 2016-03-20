__author__ = 'QHe'


def get_anagrams(filename):
    """
    Map each word to a list of its anagrams.
    """
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = ''.join(sorted(list(word)))
        d.setdefault(t, []).append(word)
    return d

def print_anagrams_in_order(d):
    t = []
    for v in d.values():
        if len(v) > 1:
            t.append((len(v), v))

    for x in sorted(t):
        print x


def filter_length(d, n):
    """
    Map the words with n letters to their lists of anagrams
    """
    res = {}
    for word, anagrams in d.iteritems():
        if len(word) == n:
            res[word] = anagrams
    return res


if __name__ == '__main__':
    d = get_anagrams('words.txt')
    print_anagrams_in_order(d)

    print_anagrams_in_order(filter_length(d, 8))