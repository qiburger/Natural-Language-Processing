__author__ = 'Qi_He'

__author__ = 'Qi_He'


import os
import collections
import math
from operator import itemgetter
import pickle

backgound_root = '../data/train/background.txt'
objective_root = '../data/train/objective.txt'
methods_root = '../data/train/methods.txt'
results_root = '../data/train/results.txt'
train_dir_root = '../data/train'
samples_root = '../data/test/samples.txt'
excerpt_path = '../data/clustering/excerpts.txt'

from tokenization import *


'''
    TF-IDF
'''

'''
    TF-IDF: TF gives high weights to terms that are frequent
    IDF penalizes weights of terms that are common across many samples in corpus
'''
# return a dict of the freq of words in the input (tokenized list)
# Counter objects in colletions is used
def get_tf(sample):
    return collections.Counter(sample)

# return a dict of words in corpus and corresponding IDF
def get_idf(corpus):
    idf_dict = {}
    df_dict = collections.defaultdict(int)
    num_of_excerpts = len(corpus)
    keys = set(flatten((corpus)))
    for words in keys:
        for excerpts in corpus:
            if words in excerpts:
                df_dict[words] += 1
    for items in df_dict:
        idf_dict[items] = math.log(float(num_of_excerpts) / df_dict[items])
    return idf_dict

# return a dict of words and corresponding tfidf weights
def get_tfidf(tf_dict, idf_dict):
    tfidf = {}
    intsect_keys = list(set(tf_dict.keys()) & set(idf_dict.keys()))
    for tf_keys in intsect_keys:
        tfidf[tf_keys] = float(tf_dict[tf_keys]) * float(idf_dict[tf_keys])
    return tfidf

# takes TF and IDF dicts and gives a list of tuples containing
# k words with highest weight and corresponding TF-IDF values
def get_tfidf_weights_topk(tf_dict, idf_dict, k):
    tfidf = get_tfidf(tf_dict, idf_dict)
    return sorted(tfidf.iteritems(), key=itemgetter(1), reverse=True)[:k]

# like get_idf, but only for words in sample
def get_idf_for_sample(sample, corpus):
    idf_dict = {}
    df_dict = collections.defaultdict(int)
    num_of_excerpts = len(corpus)
    keys = set(sample)
    for words in keys:
        for excerpts in corpus:
            if words in excerpts:
                df_dict[words] += 1
    for items in df_dict:
        idf_dict[items] = math.log(float(num_of_excerpts) / df_dict[items])
    return idf_dict

# get tf-idf for each word and return a list of tuples
def get_tfidf_topk(sample, corpus, k):
    tf_dict = get_tf(sample)
    idf_dict = get_idf_for_sample(sample, corpus)
    return get_tfidf_weights_topk(tf_dict,idf_dict,k)

# write words and corresponding weighting into txt
def write_output(filename, tuple_list):
    fout = open(filename,"w")
    for (word, freq) in tuple_list:
        fout.write(word + "\t" + str(freq) + "\n")
    fout.close()

# Run TF-IDF and write output
def run_tf_idf():
    filename_a = "hw1_2-1a.txt"
    filename_b = "hw1_2-1b.txt"
    sample = flatten(load_file_excerpts(backgound_root))
    corpus = load_file_directory_excerpts(train_dir_root)

    tfidf_list = get_tfidf_topk(sample, corpus, k=1000)
    write_output(filename_a, tfidf_list)

    idf_dict = get_idf(corpus)
    pickle.dump(idf_dict, open('corpus_idf.p', 'wb'))
    write_output(filename_b, idf_dict.iteritems())

    return tfidf_list

def shortcut_tf_idf():

    filename_a = "hw1_2-1a.txt"
    filename_b = "hw1_2-1b.txt"

    sample = flatten(load_file_excerpts(backgound_root))

    idf_dict = pickle.load(open('corpus_idf.p','rb'))
    tf_dict = get_tf(sample)
    tfidf_list = get_tfidf_weights_topk(tf_dict,idf_dict,1000)

    write_output(filename_a, tfidf_list)
    write_output(filename_b, idf_dict.iteritems())

    return tfidf_list


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


'''
    Precision and Recall
'''
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


'''
    Cosine Similarity
'''

# calculate cosine similarity of two lists of integers
def cosine_sim(l1, l2):

    if all(x == 0 for x in l1) or all(y == 0 for y in l2):
        return 0
    xx = 0
    yy = 0
    xy = 0
    for i in range(len(l1)):
        x = l1[i]
        y = l2[i]
        xy += x * y
        xx += x ** 2
        yy += y ** 2
    return xy / math.sqrt(xx * yy)

'''
    Labeling New Excerpts
'''

# create vector space (dict) of a list of strings
def create_feature_space(list):
    feature_space = {}
    count = 0
    for words in list:
            if words not in feature_space:
                feature_space[words] = count
                count += 1
    return feature_space

def vectorize_tfidf(feature_space, idf_dict, sample):
    vector = []
    tf_dict = get_tf(sample)
    for w in feature_space.keys():
        if w not in tf_dict:
            vector.append(0)
        else:
            vector.append(float(tf_dict[w]) * idf_dict[w])
    return vector

def get_section_representations(dirname, idf_dict, feature_space):
    section_rep = {}
    for dirpath, dirnames, filenames in os.walk(dirname):
        for files in filenames:
            sample = flatten(load_file_excerpts(os.path.join(dirname,files)))
            vector = vectorize_tfidf(feature_space, idf_dict, sample)
            section_rep[files] = vector
    return section_rep

def predict_class(excerpt, representation_dict, feature_space, idf_dict):
    global filename
    excerpt_vector = vectorize_tfidf(feature_space, idf_dict, excerpt)
    similarity = 0.0
    for keys, vectors in representation_dict.iteritems():
        new_cos = cosine_sim(vectors, excerpt_vector)
        if new_cos > similarity:
            similarity = new_cos
            filename = keys
    return filename

def label_sents(excerptfile, outputfile):
    list_of_excerpts = load_file_excerpts(excerptfile)
    idf_dict = pickle.load(open('corpus_idf.p','rb'))
    dirname = train_dir_root
    corpus = load_file_directory_excerpts(train_dir_root)

    word_list = []
    tf_dict = get_tf(flatten(corpus))
    tfidf = get_tfidf(tf_dict, idf_dict)
    for words, weight in sorted(tfidf.iteritems(), key=itemgetter(1), reverse=True)[:1000]:
        word_list.append(words)

    feature_space = create_feature_space(word_list)
    section_rep = get_section_representations(dirname, idf_dict, feature_space)
    pickle.dump(section_rep, open('section_rep.p','wb'))

    fout = open(outputfile,"w")

    for excerpts in list_of_excerpts:
        file_section = predict_class(excerpts,section_rep,feature_space,idf_dict).split(".")[0]
        fout.write(file_section + "\n")

    fout.close()

def run_labeling():
    label_sents(samples_root,"hw1_4.txt")


'''
    Clustering Excerpts
'''

# returns a list of the union of sets of words returned by get_mi_topk(file,corpus,k)
# for each file in dirname
def generate_mi_feature_labels(dirname, k, corpus):
    output_list = []
    file_list = load_file_directory_excerpts(dirname)
    word_probs = get_word_probs(flatten(corpus))
    pickle.dump(word_probs, open('word_probs.p', 'wb'))

    n = 5.0 / len(flatten(corpus))

    for files in file_list:
        mi_dict = {}
        conditional_dict = get_word_probs(files)
        corpus_dict = word_probs
        for keys in conditional_dict:
            if corpus_dict[keys] >= n:
                mi_dict[keys] = math.log(conditional_dict[keys] / corpus_dict[keys])
        mi_list = sorted(mi_dict.iteritems(), key=itemgetter(1), reverse=True)[:k]

        for words, weights in mi_list:
            output_list.append(words)
    return list(set(output_list))

def generate_tfidf_feature_labels(corpus, k, idf_dict):
    output_set = set()

    tf_dict = get_tf(flatten(corpus))
    tfidf_list = get_tfidf_weights_topk(tf_dict,idf_dict,k)
    for words, weights in tfidf_list:
        output_set = output_set | {words}
    return list(output_set)

def vectorize_mi(feature_space, word_probs, sample):
    vector = []

    mi_dict = {}
    conditional_dict = get_word_probs(sample)
    corpus_dict = word_probs

    for w in feature_space.keys():
        if w not in conditional_dict:
            vector.append(0)
        else:
            vector.append(math.log(float(conditional_dict[w]) / corpus_dict[w]))
    return vector

def prepare_cluto_tfidf(samplefile, labelfile, matfile, corpus):

    labelfile_out = open(labelfile, "w")
    matfile_out = open(matfile, "w")

    idf_dict = pickle.load(open('corpus_idf.p','rb'))

    word_list = generate_tfidf_feature_labels(corpus, 1000, idf_dict)
    for words in word_list:
        labelfile_out.write(str(words) + "\n")

    sample_list = load_file_excerpts(samplefile)
    feature_space = create_feature_space(word_list)

    matfile_out.write(str(len(sample_list)) + " " + str(len(word_list))+"\n")

    for samples in sample_list:
        vector = vectorize_tfidf(feature_space, idf_dict, samples)
        for weights in vector:
            matfile_out.write(str(weights) + " ")
        matfile_out.write("\n")

    labelfile_out.close()
    matfile_out.close()

def prepare_cluto_mi(samplefile, labelfile, matfile, corpus):
    labelfile_out = open(labelfile, "w")
    matfile_out = open(matfile, "w")

    word_list = generate_mi_feature_labels(train_dir_root, 1000, corpus)
    for words in word_list:
        labelfile_out.write(str(words) + "\n")

    sample_list = load_file_excerpts(samplefile)
    feature_space = create_feature_space(word_list)
    word_probs = pickle.load(open('word_probs.p','rb'))

    matfile_out.write(str(len(sample_list)) + " " + str(len(word_list))+"\n")

    for samples in sample_list:
        vector = vectorize_mi(feature_space, word_probs, samples)
        for weights in vector:
            matfile_out.write(str(weights) + " ")
        matfile_out.write("\n")

    labelfile_out.close()
    matfile_out.close()

def run_clustering():
    corpus = load_file_directory_excerpts(train_dir_root)
    #prepare_cluto_tfidf(excerpt_path,'labelfile_tfidf.txt','matfile_tfidf.txt',corpus)
    prepare_cluto_mi(excerpt_path,'labelfile_mi.txt','matfile_mi.txt',corpus)


'''
    Importanat note:
    Always run run_tf_idf() at least once to generate idf_dict
'''

if __name__ == "__main__":


    #run_tf_idf()
    #run_mi()
    #run_prec_rec()
    #run_labeling()
    run_clustering()










    #print get_all_files('/Users/Qi_He/Desktop/2015')
    #print standardize("TThis is a test!! try it *&*")
    #print load_file_excerpts('/Users/Qi_He/Desktop/2015/CIS 530/hw1_heqi/emma.txt')
    #print load_file_directory_excerpts('/Users/Qi_He/Desktop/2015/CIS 530/hw1_heqi')
    #print get_tf(["test1", "test2","test","a","b","a"])
    #print get_tfidf({},{})
    #print get_tfidf_weights_topk({"a":3.0, "b":4.0},{"a":0.3, "b":0.25},1)
    #print get_idf([["a","b","c"],["b","c"],["d","e"]])
    #print get_tfidf_topk(["a","b","c","d","e","a"],[["a","a","b","c","d","e"],["b","c","a","b"],["d","e"]],5)
    #tfidf_list = get_tfidf_topk(["a","b","c","d","e","a"],[["a","a","b","c","d","e"],["b","c","a","b"],["d","e"]],5)
    #write_output(filename, tfidf_list)






