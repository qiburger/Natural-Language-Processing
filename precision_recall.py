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
from mutual_info import *

# get precision of l1 using l2 as a reference
def get_precision(l1, l2):
    intsect_keys = list(set(l1) & set(l2))
    return float(len(intsect_keys)) / len(l1)

# get recall of l1 using l2 as a reference
def get_recall(l1, l2):
    intsect_keys = list(set(l1) & set(l2))
    return float(len(intsect_keys)) / len(l2)

# run precision and recall with top 1000 MI & TF-IDF words

def run_prec_rec():
    l1 = []
    l2 = []
    mi_list = run_mi()
    tfidf_list = shortcut_tf_idf()

    for words, weight in mi_list:
        l1.append(words)

    for words, weight in tfidf_list:
        l2.append(words)

    precision = get_precision(l1,l2)
    recall = get_recall(l1,l2)

    fout = open("writeup.txt","w")
    fout.write("Precision: " + str(precision) + "\n")
    fout.write("Recall: " + str(recall))
    fout.close()
