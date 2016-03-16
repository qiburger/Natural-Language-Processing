from function_word_svm import *

"""
Lexical Substitution model to handle unknown POS

final model will be similar to multiclass svm model,
but instead of replacing out-of-vocabulary words with an <UNK> token,
we will replace them with the most similar word in the vocabulary based on
cosine similarity of word2vec word embedding vectors.
Here we wish to see if replacing infrequent words with similar,
but more frequent, words, will lead to improved POS tagging performance.
"""


def lex_sub_dict(w2vecdict, freqwordvocab, infreqwordvocab):
    """

    :param w2vecdict: a dict with str keys and numpy array values
    :param freqwordvocab: set of infreq words
    :param infreqwordvocab: set of freq words
    :return dictionary mapping infreq to freq words by cosine similarity
    """
    out_dict = {}

    for infreq_word in infreqwordvocab:
        if infreq_word in w2vecdict:
            infreq_vector = w2vecdict[infreq_word]
            min_cosine_distance = 2
            for freq_word in freqwordvocab:
                if freq_word in w2vecdict:
                    freq_vector = w2vecdict[freq_word]
                    temp_distance = cosine_distance(infreq_vector, freq_vector)
                    if temp_distance < min_cosine_distance:
                        min_cosine_distance = temp_distance
                        closest_word = freq_word
            out_dict[infreq_word] = closest_word
    return out_dict


def get_w2vec(w2vec_file_location):
    """
    :param w2vec_file_location: read a word2vec file
    :return: a dict with str keys and numpy array values
    """
    dict_out = {}
    with open(w2vec_file_location, "r") as fin:
        for line in fin:
            first_split = line.split()
            token = first_split[0]
            vector_list = first_split[1].split(",")
            vector = np.array(map(float, vector_list))
            dict_out[token] = vector
    return dict_out


def write_word_pairs():
    word_list = []
    with open("/home1/c/cis530/hw3/data/wordlist.txt", "r") as fin:
        for line in fin:
            word_list.append(line.strip())
    vocab = build_vocab(training_directory)
    w2vec_dict = get_w2vec(wordtovec)
    out_dict = lex_sub_dict(w2vec_dict, vocab, word_list)
    with open("hw_3_5.txt", "w") as fout:
        for token in word_list:
            fout.write(token)
            fout.write("\t")
            if token in out_dict:
                fout.write(out_dict[token])
            fout.write("\n")


def prep_data_lexsub(dirname, outfile, windowsize, tagmap, vocab, w2vecdict):
    """"
    :param dirname: path to a directory containing one or more raw POS-tagged files.
    :param outfile: write output file
    :param windowsize: given (always odd int)
    :param tagmap: PTB to google tags
    :param vocab: set of vacab we can recognize
    :param w2vecdict: for infreq/unseen words, replace with nearest words. If no nearest words avail, use <UNK>
    :return list of (tag, [context])
    """
    file_list = get_all_files(dirname)
    out_list = []
    word_replacement_dict = {}
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
                            if temp_word in w2vecdict:
                                if temp_word in word_replacement_dict:
                                    temp_list.append(word_replacement_dict[temp_word])
                                else:
                                    temp_replacement_dict = lex_sub_dict(w2vecdict, vocab, [temp_word])
                                    word_replacement_dict[temp_word] = temp_replacement_dict[temp_word]
                                    temp_list.append(word_replacement_dict[temp_word])
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


def run_model_three():
    """
    Run model three with vocab as words that appeared at least 8 times and context window of 3

    """

    pos_map = pickle.load(open('pos_map.p', "rb"))
    vocab = build_vocab(training_directory)
    word2vec = get_w2vec(wordtovec)

    train_out_list = prep_data_lexsub(training_directory, "mod3_train_prepped.txt", 3, pos_map, vocab, word2vec)
    test_out_list = prep_data_lexsub(testing_directory, "mod3_test_prepped.txt", 3, pos_map, vocab, word2vec)

    posset = get_posset()
    vocab.add("<s>")
    vocab.add("<UNK>")
    convert_to_svm('mod3_train_prepped.txt', "mod3_train.svm", posset, vocab)
    convert_to_svm('mod3_test_prepped.txt', "mod3_test.svm", posset, vocab)

    p_labels, p_acc, p_vals = train_test_model("mod3_train.svm", "mod3_test.svm")
    with open("modelscores.txt", "a") as text_file:
        text_file.write(str(p_acc[0]))
        text_file.write("\n")
    pickle.dump(p_labels, open('mod3_p_labels.p', 'wb'))
