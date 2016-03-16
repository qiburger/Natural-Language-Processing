# coding=utf-8
from baseline_model import *

"""


we will be using the libsvm library to implement a multi-class prediction support vector machine with a linear kernel.
Given a training set of sentences with POS-tagged tokens,
we would like to train a model to predict the POS tags of words in new sentences.

Our feature space: Throughout the next three sections
we will experiment with variations on the following feature set for our data.
We represent each token t in our dataset as a numeric feature vector of length V ×W ,
where V is the size of our vocabulary, and W is the size of our context window, an odd positive integer.

We use the context window to incorporate information about the words surrounding token t
when we make our prediction about the POS tag for t.
Each word in our feature vocabulary is mapped to a unique integer index 1 < i ≤ V .
If we give each token in our context window a position n with 0 < n < W,
the value of element nV +i in our vector is equal to 1
if the nth word in our context window corresponds to index i, and 0 otherwise.
Our target token (for which we are making the tag prediction) is always in the center of the context window.
Our first model will use a window size W = 3.
Our vocabulary will consist of all tokens in files within the data/train directory that occur at least eight times.

"""


def prep_data(dirname, outfile, windowsize, tagmap, vocab):
    """

    :param dirname: path to a directory containing one or more raw POS-tagged files.
    :param outfile: write output file
    :param windowsize: given (always odd int)
    :param tagmap: PTB to google tags
    :param vocab: set of vacab we can recognize
    :return list of (tag, [context])
    """
    file_list = get_all_files(dirname)
    out_list = []
    for file_in in file_list:
        list_of_sent = parse_taggedfile(file_in, tagmap)
        for sentence in list_of_sent:
            for i in range(len(sentence)):
                temp_list = []
                for j in range(windowsize):
                    offset = j - (windowsize + 1) / 2 + 1
                    if (i + offset) < 0 or (i + offset) >= len(sentence):
                        temp_list.append("<s>")
                    else:
                        temp_word = sentence[i + offset][0]
                        if temp_word in vocab:
                            temp_list.append(temp_word)
                        else:
                            temp_list.append("<UNK>")
                out_list.append((sentence[i][1], temp_list))
    with open(outfile, "w") as fout:
        for key, word_list in out_list:
            fout.write(key)
            fout.write("\t")
            for items in word_list:
                fout.write(items)
                fout.write(" ")
            fout.write("\n")
    return out_list


def build_vocab(training_location):
    """
    Get a set of words that occurred at least 8 times in training wsj files
    :param training_location: directory of all training wsj files
    :return: set of words that occurred 8+ times
    """
    vocab_list = []
    for trainin_file in get_all_files(training_location):
        token_tag_list = flatten(parse_taggedfile(trainin_file, {}))
        for token, tag in token_tag_list:
            vocab_list.append(token)
    vocab_hist = Counter(vocab_list)
    set_out = set()
    for key in vocab_hist:
        if vocab_hist[key] > 7:
            set_out.add(key)
    pickle.dump(set_out, open("vocab.p", "wb"))
    return set_out


def write_100_lines(input_file, output_file):
    """
    Write the first 100 lines of the
    :param input_file:
    :param output_file:
    """
    with open(input_file, "r") as fin:
        with open(output_file, "w") as fout:
            counter = 0
            for line in fin:
                if counter < 100:
                    fout.write(line)
                counter += 1


def run_prep_data():
    """
        Run twice: once for training data, once for testing data.

    """
    pos_map = pickle.load(open('pos_map.p', "rb"))
    vocab_set = build_vocab(training_directory)
    train_out_list = prep_data(training_directory, "mod1_train_prepped.txt", 3, pos_map, vocab_set)
    pickle.dump(train_out_list, open('mod1_train_prep.p', 'wb'))

    test_out_list = prep_data(testing_directory, "mod1_test_prepped.txt", 3, pos_map, vocab_set)
    pickle.dump(test_out_list, open('mod1_test_prep.p', 'wb'))

    write_100_lines("mod1_train_prepped.txt", "hw_3_3_1.txt")


def convert_to_svm(preppedfile, outfile, posset, vocab):
    vocab_index_list = [i + 1 for i in range(len(vocab))]
    sorted_vocab = sorted(list(vocab))
    v = len(sorted_vocab)
    vocab_dict = dict(zip(sorted_vocab, vocab_index_list))

    posset_index_list = [i + 1 for i in range(len(posset))]
    sorted_posset = sorted(list(posset))
    posset_dict = dict(zip(sorted_posset, posset_index_list))

    with open(preppedfile, "r") as fin:
        with open(outfile, "w") as fout:
            for line in fin:
                sentence = line.split()

                fout.write(str(posset_dict[sentence[0]]))
                fout.write("\t")

                for i in range(len(sentence)):
                    if i >0:
                        fout.write(str((i-1) * v + vocab_dict[sentence[i]]))
                        fout.write(":")
                        fout.write("1")
                        fout.write(" ")

                    '''
                    if i > 0:
                        for tokens in vocab_dict:
                            if tokens == right_token:
                                fout.write(str(vocab_dict[tokens]))
                                fout.write(":")
                                fout.write("1")
                            else:
                                fout.write(str(vocab_dict[tokens]))
                                fout.write(":")
                                fout.write("0")
                            fout.write(" ")
                        '''
                fout.write("\n")


def get_posset():
    """
    Load the previously pickled pos_map dictionary and return the set of Google POS tags
    :return: set of Google tags
    """
    pos_dict = pickle.load(open('pos_map.p', "rb"))
    out_set = set(pos_dict.values())
    return out_set


def run_svm_conversion():
    posset = get_posset()
    vocab = pickle.load(open("vocab.p", "rb"))
    vocab.add("<s>")
    vocab.add("<UNK>")
    convert_to_svm('mod1_train_prepped.txt', "mod1_train.svm", posset, vocab)
    print "train done"
    convert_to_svm('mod1_test_prepped.txt', "mod1_test.svm", posset, vocab)
    print "test done"



'''
    Training and testing
'''


def train_test_model(train_datafile, test_datafile):
    """
    Train and test using libsvm for model 1
    :param train_datafile:
    :param test_datafile:
    """
    y, x = svm_read_problem(train_datafile)
    m = svm_train(y, x, '-t 0 -e .01 -m 1000 -h 0')
    test_y, test_x = svm_read_problem(test_datafile)
    return svm_predict(test_y, test_x, m)


def run_model_one():
    p_labels, p_acc, p_vals = train_test_model("mod1_train.svm", "mod1_test.svm")
    with open("modelscores.txt", "a") as text_file:
        text_file.write(str(p_acc[0]))
        text_file.write("\n")
    pickle.dump(p_labels, open('mod1_p_labels.p', 'wb'))