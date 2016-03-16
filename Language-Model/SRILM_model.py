from build_language_model import *

'''
    Building a language model with SRILM

    Use SRILM ngram program to calculate the perplexity of a language model for a given text.
    Perplexity tells us about the length-normalized likelihood of a text.
    In other words, the larger the perplexity, the more surprising is a given text under a language model.

'''


def srilm_preprocess(raw_text, temp_file):
    sent_list = tokenize_sentence(raw_text)
    fout = open(temp_file, "w")
    for sentences in sent_list:
        fout.write(sentences + '\n')
    fout.close()


def srilm_bigram_models(input_file, output_dir):
    """
    Generate lm based on input file
    :param input_file: plain text file
    :param output_dir: directory to store the language model
    """
    input_basename = os.path.basename(input_file)

    # set the path of the processed input excerpt as input_file_process.txt in the same directory.
    processed_text_path = os.path.join(output_dir, (os.path.splitext(input_basename)[0] + "_processed.txt"))

    input_text = open(input_file, "r").read()
    srilm_preprocess(input_text, processed_text_path)

    unigram_path = os.path.join(output_dir, (input_basename) + '.uni.lm')
    unigram_count_path = os.path.join(output_dir, (input_basename) + '.uni.counts')

    bigram_path = os.path.join(output_dir, (input_basename) + '.bi.lm')
    bigram_kn_path = os.path.join(output_dir, (input_basename) + '.bi.kn.lm')

    # 1. unigram
    unigram_pipe = Popen(
        ['/home1/c/cis530/srilm/ngram-count', '-order', '1', '-addsmooth', '0.25', '-text', processed_text_path, '-lm',
         unigram_path], stdout=PIPE)
    unigram_count_pipe = Popen(
        ['/home1/c/cis530/srilm/ngram-count', '-order', '1', '-addsmooth', '0.25', '-text', processed_text_path,
         '-write', unigram_count_path], stdout=PIPE)

    # 2. bigram
    bigram_pipe = Popen(
        ['/home1/c/cis530/srilm/ngram-count', '-order', '2', '-addsmooth', '0.25', '-text', processed_text_path, '-lm',
         bigram_path], stdout=PIPE)

    # 3. bigram with KN smoothing
    bigram_kn_pipe = Popen(
        ['/home1/c/cis530/srilm/ngram-count', '-order', '2', '-kndiscount', '-text', processed_text_path, '-lm',
         bigram_kn_path], stdout=PIPE)


def write_100_lines(input_file):
    with open(input_file, 'r') as fin:
        fout = open(input_file + "_100.txt", 'w')
        for lines in fin:
            fout.write(lines)
        fout.close()


def srilm_ppl(model_file, raw_text):
    temp_text_path = os.getcwd() + '/temp_excerpt.txt'
    srilm_preprocess(raw_text, temp_text_path)

    pipe = Popen(['/home1/c/cis530/srilm/ngram', '-lm', model_file, '-ppl', temp_text_path], stdout=PIPE)

    # find ppl in output
    ppl = ''
    output_list = pipe.communicate()[0].split(' ')

    for index, item in enumerate(output_list):
        if item == 'ppl=':
            ppl = output_list[index + 1]
    return float(ppl)


def run_srilm():
    output_dir = '/home1/h/heqi/cis530/hw2_heqi/models'
    for filepaths in get_all_files('/home1/c/cis530/hw2/data/train'):
        srilm_bigram_models(filepaths, output_dir)
    for models in get_all_files(output_dir):
        write_100_lines(models)
