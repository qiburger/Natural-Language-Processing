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

