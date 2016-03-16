from wordnet_topic_words import *

"""
We use a dependency parser to expand our list of topic words with their descriptors.
The Stanford Parser is an off-the-shelf statistical parser that can output dependency relationships.
We will use the Stanford Parser to find all modifiers for the topic words in a given document cluster.
We will then expand the list of topic words to include all modifiers.
"""

def expand_keywords_dp(keylist, input_dir, outputfile):
    parse_list = do_lexparse(input_dir)
    out_list = []
    for keys in keylist:
        temp_list = [keys]
        for index in range(len(parse_list)):
            if parse_list[index] == keys:
                if parse_list[index+3] == '\n':
                    temp_word = parse_list[index-2]
                    if temp_word not in temp_list:
                        temp_list.append(temp_word)
                else:
                    temp_word = parse_list[index+2]
                    if temp_word not in temp_list:
                        temp_list.append(temp_word)
        out_list.append(temp_list)
    with open(outputfile, "w") as fout:
        for lines in out_list:
            fout.write(lines[0])
            if len(lines) > 1:
                fout.write('\t')
                fout.write(lines[1])
                for i in range(len(lines)):
                    if i > 1:
                        fout.write(',')
                        fout.write(lines[i])
            fout.write('\n')


def get_all_files(directory):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list


def do_lexparse(input_dir):
    raw_list = []
    output_list = []
    dev_list = get_all_files(input_dir)
    for dev_file in dev_list:
        pipe = Popen([lex_parser_addr, dev_file], stdout=PIPE)
        for line in pipe.communicate()[0].split('\n'):
            raw_list.append(line)
            output_list.extend(re.split(', |\(|\)|\-[0-9]+', line))
            output_list.append("\n")
    return output_list