__author__ = 'Qi_He'


# return relative file paths for all files in the input directory
def get_all_files(directory):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            relDir = os.path.relpath(dirpath, directory)
            file_list.append(os.path.join(relDir, filename))
    return file_list

# converts a string input to lowercase and splits into tokens
def standardize(rawexcerpt):
    decoded_list = word_tokenize(rawexcerpt.lower().decode('utf8'))
    return [word.encode('utf8') for word in decoded_list]

# returns a list of all excerpts under an absolute path, tokenized and lower-cased
def load_file_excerpts(filepath):
    list_out = []
    fin = open(filepath, 'r')
    for line in fin:
        list_out.append(standardize(line))
    fin.close()
    return list_out

# returns list of all excerpts from files under one directory, concatenated
def load_file_directory_excerpts(dirpath):
    if os.path.isdir(dirpath):
        list_out = []
        for files in get_all_files(dirpath):
            list_out.append(load_file_excerpts(os.path.join(dirpath,files)))
        return flatten(list_out)
    else:
        load_file_excerpts(dirpath)

# flatten 2-d list of lists to 1-d list
def flatten(listoflists):
    return list(itertools.chain(*listoflists))