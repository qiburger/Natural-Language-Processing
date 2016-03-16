from expand_topic_dp import *

"""
We will build 2 summarizers: a simple baseline and a greedy summarizer based on KL divergence

"""


def summarize_baseline(directory, outputfile):
    output_list = []
    counter = 0
    file_list = get_all_files(directory)
    for files in file_list:
        with open(files, "r") as fin:
            if counter < 100:
                first_sent = fin.readline().rstrip()
                temp_list = tokenize(first_sent)
                output_list.append(first_sent)
                counter += len(temp_list)
    with open(outputfile, "w") as fout:
        for sent in output_list:
            fout.write(sent)
            fout.write('\n')


def tokenize(rawexcerpt):
    """
    :param Rawexcerpt: string input
    :return: Tokenized list of words (maintain capitalized letters)
    """
    decoded_list = word_tokenize(rawexcerpt.decode('utf8'))
    return [word.encode('utf8') for word in decoded_list]


def check_size():
    folder_list = []
    for i in range(40):
        if i < 10:
            folder_list.append(dev_input + "/dev_0" + str(i))
        else:
            folder_list.append(dev_input + "/dev_" + str(i))
    print folder_list
    for directory in folder_list:
        output_list = []
        file_list = get_all_files(directory)
        for files in file_list:
            with open(files, "r") as fin:
                if len(output_list) < 100:
                    output_list.extend(tokenize(fin.readline().rstrip()))
        if len(output_list) < 100:
            print output_list
            print "error"


def word_counter(file_in):
    output_list = []
    with open(file_in, "r") as fin:
        for line in fin:
            temp_list = tokenize(line.rstrip())
            output_list.extend(temp_list)
    print output_list
    print len(output_list)


def do_baseline():
    folder_list = []
    for i in range(40):
        if i < 10:
            folder_list.append(dev_input + "/dev_0" + str(i))
        else:
            folder_list.append(dev_input + "/dev_" + str(i))
    for directory in folder_list:
        name_string = "./baseline/sum_" + directory[-6:] + ".txt"
        summarize_baseline(directory, name_string)


"""
    KL Divergence summarizer
"""


def summarize_kl(inputdir, outputfile):
    input_cluster = []
    file_list = get_all_files(inputdir)
    stop_list = get_stoplist()

    for files in file_list:
        with open(files, 'r') as fin:
            for line in fin:
                for word in tokenize(line):
                    if word not in stop_list:
                        input_cluster.append(word)
    q = Counter(input_cluster)
    q_total = sum(q.values())
    for key in q:
        q[key] /= float(q_total)
    summary = kl_greedy_helper(file_list, q, stop_list)
    with open(outputfile, "w") as fout:
        for sent in summary:
            fout.write(sent)
            fout.write('\n')


def kl_greedy_helper(file_list, q_dict, stop_list):
    summary = []
    sent_list = []
    counter = 0
    for files in file_list:
        with open(files, 'r') as fin:
            for line in fin:
                sent_list.append(line.rstrip())
    while counter <= 100:
        min_kl = 1000000
        min_sent = ""
        for sent in sent_list:
            temp_list = summary + [sent]
            p = get_p(temp_list, stop_list)
            kl = 0
            for token in p:
                kl += p[token] * math.log(p[token] / q_dict[token])
            if kl < min_kl:
                min_kl = kl
                min_sent = sent
        summary.append(min_sent)
        counter += len(tokenize(min_sent))
    return summary


def get_p(summary, stop_list):
    tokenized_list = []
    for sent in summary:
        token_list = tokenize(sent)
        for token in token_list:
            if token not in stop_list:
                tokenized_list.append(token)
    p = Counter(tokenized_list)
    p_total = sum(p.values())
    for key in p:
        p[key] /= float(p_total)
    return p


def get_stoplist():
    out_list = []
    with open("/home1/c/cis530/hw4/stopwords.txt", "r") as fin:
        for line in fin:
            out_list.append(line.rstrip())
    return out_list


def do_kl():
    folder_list = []
    for i in range(40):
        if i < 10:
            folder_list.append(dev_input + "/dev_0" + str(i))
        else:
            folder_list.append(dev_input + "/dev_" + str(i))
    for directory in folder_list:
        name_string = "./KL/sum_" + directory[-6:] + ".txt"
        summarize_kl(directory, name_string)
