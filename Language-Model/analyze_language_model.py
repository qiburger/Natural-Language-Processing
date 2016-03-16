from language_model_prediction import *

'''
    Analyzing language models
'''


def analyze_lm():
    """
    Compare the number of unique tokens, fraction of frequent and rare tokens in the training data for each excerpt type
    """
    type_list = ['background', 'objective', 'methods', 'results', 'conclusions']
    with open('vocabularySize.txt', 'w') as fout:
        for types in type_list:
            fin = open('/home1/h/heqi/cis530/hw2_heqi/models/' + types + '.txt.uni.counts', 'r')

            freq_count = 0
            rare_count = 0
            for i, l in enumerate(fin):
                content = l.split()
                if int(content[1]) > 5:
                    freq_count += 1
                elif int(content[1]) == 1:
                    rare_count += 1

            vocab_size = i + 1
            frac_freq = freq_count / float(vocab_size)
            frac_rare = rare_count / float(vocab_size)
            fout.write(types + ',' + str(vocab_size) + ',' + str(frac_freq) + ',' + str(frac_rare) + ',' + '\n')


def get_entropy(unigram_model_file, unigram_counts_file):
    """
    Entropy is a measure of uncertainty.
    A uniform word distribution in which each word is equally likely will have the highest entropy.
    The lower the entropy for a sample of text,
    the more evidence we have that certain words would be expected to occur much more often than others.

    This function calculates the entropy of a given unigram model.
    """
    entropy = 0.0

    model_file = open(unigram_model_file, 'r')
    log_prob_dict = {}
    for lines in model_file:

        line_list = lines.split()
        try:
            prob = float(line_list[0])
            log_prob_dict[line_list[1]] = prob

        except:
            pass

    count_file = open(unigram_counts_file, 'r')

    total_words = 0
    count_dict = {}
    for rows in count_file:
        content = rows.split()
        total_words += int(content[1])
        count_dict[content[0]] = int(content[1])

    for tokens in count_dict:
        if tokens in log_prob_dict:
            entropy += - (count_dict[tokens] / float(total_words) * log_prob_dict[tokens])

    model_file.close()
    count_file.close()

    return entropy


def run_entropy():
    type_list = ['background', 'objective', 'methods', 'results', 'conclusions']

    with open('hw2_4_2.txt', 'w') as fout:
        entropy_list = []
        for types in type_list:
            model_in = '/home1/h/heqi/cis530/hw2_heqi/models/' + types + '.txt.uni.lm'
            count_in = '/home1/h/heqi/cis530/hw2_heqi/models/' + types + '.txt.uni.counts'

            entropy_list.append((types, get_entropy(model_in, count_in)))
        sorted_list = sorted(entropy_list, key=operator.itemgetter(1), reverse=False)

        for name, entropy in sorted_list:
            fout.write(name + '\n')


def get_type_token_ratio(unigram_counts_file):
    count_file = open(unigram_counts_file, 'r')

    total_words = 0
    for i, l in enumerate(count_file):
        content = l.split()
        total_words += int(content[1])
    return (i + 1) / float(total_words)


def run_ttr():
    type_list = ['background', 'objective', 'methods', 'results', 'conclusions']

    with open('hw2_4_3.txt', 'w') as fout:
        out_list = []
        for types in type_list:
            count_in = '/home1/h/heqi/cis530/hw2_heqi/models/' + types + '.txt.uni.counts'
            out_list.append((types, get_type_token_ratio(count_in)))
        sorted_list = sorted(out_list, key=operator.itemgetter(1), reverse=False)

        for name, ttr in sorted_list:
            fout.write(name + '\n')
