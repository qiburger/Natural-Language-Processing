from multiclass_svm import *

"""
wider context window and very small vocabulary comprising only the most frequent words in our corpus.
Since the most frequent words in English tend to be function words,
our objective is to see how much these function words alone can tell us about parts of speech within an entire sentence.

"""

'''
    Only 100 most freq words with 7 window length
'''


def find_100_most_freq():
    """
    :param training_location: directory of all training wsj files
    :return: get 100 most frequent words in training data
    """
    vocab_list = []
    for trainin_file in get_all_files(training_directory):
        token_tag_list = flatten(parse_taggedfile(trainin_file, {}))
        for token, tag in token_tag_list:
            vocab_list.append(token)
    vocab_hist = Counter(vocab_list)
    first_100_tuples = sorted(vocab_hist.iteritems(), key=operator.itemgetter(1), reverse=True)[:100]
    return set([vocab for vocab, count in first_100_tuples])


def run_model_two():
    """
    This time run the model with only the 100 most frequent words as the vocab, but with 7 context

    """
    pos_map = pickle.load(open('pos_map.p', "rb"))
    vocab = find_100_most_freq()

    train_out_list = prep_data(training_directory, "mod2_train_prepped.txt", 7, pos_map, vocab)
    test_out_list = prep_data(testing_directory, "mod2_test_prepped.txt", 7, pos_map, vocab)

    posset = get_posset()
    vocab.add("<s>")
    vocab.add("<UNK>")
    convert_to_svm('mod2_train_prepped.txt', "mod2_train.svm", posset, vocab)
    convert_to_svm('mod2_test_prepped.txt', "mod2_test.svm", posset, vocab)

    write_100_lines("mod2_train.svm", "hw_3_4.txt")

    p_labels, p_acc, p_vals = train_test_model("mod2_train.svm", "mod2_test.svm")
    with open("modelscores.txt", "a") as text_file:
        text_file.write(str(p_acc[0]))
        text_file.write("\n")
