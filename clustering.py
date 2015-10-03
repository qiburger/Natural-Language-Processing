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
from cosine_sim import *
from precision_recall import *
from labeling import *

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
