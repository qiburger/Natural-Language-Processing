from topic_words import *

"""
We will use WordNet to find related topic words

Finding relatedness between topic words,
as well as finding descriptors of the topic words via dependency relations,
are a convenient way to expand the representation of the input in a more interpretable way.

"""


def cluster_keywords_wn(keylist, outputfile):
    """
    :param keylist: assume there is no duplicates in the list!!
    """
    list_out = []
    counter = 0
    for i in keylist:
        temp_list = [i]
        counter += 1
        for j in keylist[counter:]:
            if cluster_helper(i, j):
                temp_list.append(j)
                keylist.remove(j)
        list_out.append(temp_list)
    with open(outputfile, "w") as fout:
        for sub_list in list_out:
            fout.write(str(sub_list[0]))
            if len(sub_list)>1:
                for item in sub_list[1:]:
                    fout.write(",")
                    fout.write(str(item))
            fout.write("\n")


def cluster_helper(word1, word2):
    synset_list1 = wn.synsets(word1)
    synset_list2 = wn.synsets(word2)
    return set.intersection(get_synset_union(synset_list1), get_synset_union(synset_list2))


def get_hyponyms(synset_list):
    out = []
    for synset in synset_list:
        hyponym_list = synset.hyponyms()
        for hyponym in hyponym_list:
            out.append(hyponym.lemmas)
    return set(out)


def get_hypernyms(synset_list):
    out = []
    for synset in synset_list:
        hypernym_list = synset.hypernyms()
        for hypernym in hypernym_list:
            out.append(hypernym.lemmas)
    return set(out)


def get_synset_union(synset_list):
    lemmas = set([synset.lemmas for synset in synset_list])
    return lemmas | get_hypernyms(synset_list) | get_hyponyms(synset_list)


def run_wordnet_relatedness():
    cluster_keywords_wn(load_topic_words("./config/dev_10.ts", 20), "hw4_2_1.txt")


def check_dups():
    for i in range(40):
        if i < 10:
            name = "./config/dev_0" + str(i) + ".ts"
        else:
            name = "./config/dev_" + str(i) + ".ts"
        print name
        if len(load_topic_words(name, 1000000000000)) < len(set(load_topic_words(name, 1000000000000))):
            return False
