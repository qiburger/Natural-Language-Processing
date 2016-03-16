from parse_POS_tag import *

"""
Baseline: a prediction model that simply tags every token in the test set
            with its most frequent POS tag from the training set.
"""


def create_mft_dict(filelist):
    """
    :param filelist: List of string file names
    :return Dictionary with {tokens: most freq POS tag in training}
    """
    output_raw = defaultdict(list)
    output = {}
    for file_names in filelist:
        current_list = parse_taggedfile(file_names, {})
        for token, tag in flatten(current_list):
            output_raw[token].append(tag)
    for key in output_raw:
        output[key] = find_most_freq(output_raw[key])
    return output


def find_most_freq(list_in):
    """
    Find the most frequent element in a list, and solve ties by alphabetic order
    :param list: input list (e.g. list of various words)
    :return the most freq element
    """
    counts = Counter(list_in)
    return sorted(counts, key=lambda x: (-counts[x], x))[0]


def run_mft_baseline(testfilelist, mftdict, poslookup):
    """
    :param testfilelist: list of file inputs
    :param mftdict: dictionary mapping tokens to their most-frequent tag in the training data
    :param poslookup: dictionary mapping PTB tags to Google
    :return: float value of accuracy (correct tages / total predicted tags)
    """
    total_token = 0
    correct_token = 0
    for test_files in testfilelist:
        correct_prediction_dict = dict(flatten(parse_taggedfile(test_files, poslookup)))
        for token in correct_prediction_dict:
            total_token += 1
            if token not in mftdict:
                token_tag = "NOUN"
            else:
                ptb_tag = mftdict[token]
                token_tag = poslookup.setdefault(ptb_tag, "NOUN")
            if token_tag == correct_prediction_dict[token]:
                correct_token += 1
    return float(correct_token) / total_token

def get_all_files(directory):
    """
    Helper function to get all files in a directory
    :param directory: directory address
    :return: list of all file names (with abs path) in the directory
    """
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list


def create_mapping(map_location):
    """

    :param map_location: location of the PTB google tap map
    :return: PTB-google tag dictionary
    """
    pos_map = {}
    with open(map_location, "r") as map_in:
        for line in map_in:
            temp_list = line.split()
            pos_map[temp_list[0].strip("<>")] = temp_list[1].strip("<>")
    return pos_map


def run_baseline_predictions():
    """
    Run the baseline model over training data and return the accuracy of the model over testing data
    """
    training_list = get_all_files(training_directory)
    testing_list = get_all_files(testing_directory)

    mft_dict = create_mft_dict(training_list)
    pickle.dump(mft_dict, open('mft_dict.p', 'wb'))

    pos_map = create_mapping(pos_map_location)
    pickle.dump(pos_map, open('pos_map.p', 'wb'))

    accuracy = run_mft_baseline(testing_list, mft_dict, pos_map)

    with open("modelscores.txt", "a") as text_file:
        text_file.write(str(accuracy))
