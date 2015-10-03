__author__ = 'Qi_He'


backgound_root = '../data/train/background.txt'
objective_root = '../data/train/objective.txt'
methods_root = '../data/train/methods.txt'
results_root = '../data/train/results.txt'
train_dir_root = '../data/train'
samples_root = '../data/test/samples.txt'
excerpt_path = '../data/clustering/excerpts.txt'

from tokenization import *
from tf_idf import *


'''
    Mutual Information
'''
# return a dict of unique words in sample and
# est. probability of that word in sample
def get_word_probs(sample):
    dict_out = get_tf(sample)
    n = float(len(sample))
    for keys, values in dict_out.iteritems():
        dict_out[keys] = float(values) / n
    return dict_out

# get dict of words in sample and their mutual info
# p(w) is based on corpus
# ignore words that occurred < 5 times in corpus
def get_mi(sample, corpus):
    output_dict = {}
    n = 5.0 / len(flatten(corpus))
    conditional_dict = get_word_probs(sample)
    corpus_dict = get_word_probs(flatten(corpus))
    for keys in conditional_dict:
        if corpus_dict[keys] >= n:
            output_dict[keys] = math.log(conditional_dict[keys] / corpus_dict[keys])
    return output_dict

# return only top k words by MI in sample
def get_mi_topk(sample, corpus, k):
    mi_dict = get_mi(sample, corpus)
    return sorted(mi_dict.iteritems(), key=itemgetter(1), reverse=True)[:k]

# run MI scripts on sample and corpus given
def run_mi():
    filename_2 = "hw1_2-2.txt"
    sample = flatten(load_file_excerpts(backgound_root))
    corpus = load_file_directory_excerpts(train_dir_root)
    mi_list = get_mi_topk(sample, corpus, k=1000)
    write_output(filename_2, mi_list)
    return mi_list

