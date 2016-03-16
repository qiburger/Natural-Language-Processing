from lexical_substitution import *


def compare_results(actual, modAlabels, modBlabels):
    """
    :param actual: list of actual labels
    :param modAlabels: lsit of labels predicted by model A
    :param modBlabels: list of labels predicted by model B
    :return: [[a_right_b_right, a_right_b_wrong],[a_wrong_b_right, a_wrong_b_wrong]]
    """
    a_right_b_right = 0
    a_right_b_wrong = 0
    a_wrong_b_right = 0
    a_wrong_b_wrong = 0
    for i in range(len(actual)):
        if actual[i] == modAlabels[i]:
            if actual[i] == modBlabels[i]:
                a_right_b_right += 1
            else:
                a_right_b_wrong += 1
        else:
            if actual[i] == modBlabels[i]:
                a_wrong_b_right += 1
            else:
                a_wrong_b_wrong += 1
    return [[a_right_b_right, a_right_b_wrong], [a_wrong_b_right, a_wrong_b_wrong]]


def get_actual_labels():
    """
    retunr a list of labels (actual) from prepped file

    """
    list_out = []
    posset = get_posset()
    posset_index_list = [i + 1 for i in range(len(posset))]
    sorted_posset = sorted(list(posset))
    posset_dict = dict(zip(sorted_posset, posset_index_list))

    with open("mod1_test_prepped.txt") as fin:
        for line in fin:
            tag = line.split()[0]
            tag_index = posset_dict[tag]
            list_out.append(tag_index)

    return list_out


def run_compare_results():
    model_1_labels = pickle.load(open('mod1_p_labels.p', "rb"))
    model_3_labels = pickle.load(open('mod3_p_labels.p', "rb"))
    compmat = compare_results(get_actual_labels(), model_3_labels, model_1_labels)
    with open("hw_3_6.txt", 'w') as fout:
        print >> fout, compmat