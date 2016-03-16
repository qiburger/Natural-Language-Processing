from SRILM_model import *

"""
    Prediction with Language Model

    We use the bigram model with Kneser-Ney smoothing
    to predict the type of new excerpts that were not part of our training data.
"""


def lm_predict(models, test_file, pred_file):
    """
    Predicts the type of the excerpt for each line in test file using the specified language models.
    :param models: absolute path of the language model
    :param test_file: absolute path of the plain text file which we need to process
    :param pred_file: path of the file to which the predictions are written
    """
    prediction = open(pred_file, 'w')
    corpus = open(test_file, 'r')

    line_type = []

    for lines in corpus:
        ppl_dict = {}

        for (model_name, model_path) in models:
            ppl_dict[model_name] = srilm_ppl(model_path, lines)

        best_type = max(ppl_dict.iteritems(), key=operator.itemgetter(1))[0]
        if ppl_dict[best_type] == ppl_dict['conclusions']:
            best_type = 'conclusions'

        line_type.append(best_type)

    for types in line_type:
        prediction.write(types + '\n')

    prediction.close()
    corpus.close()


def confusion_matrix(labels, predictions):
    """
    Implement my own confusion matrix
    :param labels: str
    :param predictions: str
    :return: confusion matrix
    """
    classes = sorted(set(labels + predictions))
    classes_dict = dict((val, i) for (i, val) in enumerate(classes))

    # initialize matrix
    m = [[0.0 for val in classes] for val in classes]

    for lab, pred in zip(labels, predictions):
        m[classes_dict[lab]][classes_dict[pred]] += 1.0

    for rows in m:
        row_sum = sum(rows)
        for index, values in enumerate(rows):
            if row_sum != 0:
                rows[index] = values / row_sum
    return m


def not_normalized_cm(labels, predictions):
    classes = sorted(set(labels + predictions))
    classes_dict = dict((val, i) for (i, val) in enumerate(classes))

    # initialize matrix
    m = [[0.0 for val in classes] for val in classes]

    for lab, pred in zip(labels, predictions):
        m[classes_dict[lab]][classes_dict[pred]] += 1.0

    return m


def evaluate(label_file, pred_file):
    """
    Evaluate the accuracy and confusion matrix
    """
    labels = []
    predictions = []
    with open(label_file, 'r') as label_text:
        for rows in label_text:
            labels.append(rows.rstrip('\n'))

    with open(pred_file, 'r') as pred_text:
        for rows in pred_text:
            predictions.append(rows.rstrip('\n'))

    cm = not_normalized_cm(labels, predictions)
    normalized_cm = confusion_matrix(labels, predictions)

    total_count = sum(sum(lists) for lists in cm)
    accuracy = sum(cm[i][i] for i in range(len(cm))) / float(total_count)

    return accuracy, normalized_cm


def run_lm_predict():
    accuracy_list = []

    # 1.1 bigram KN
    model_list = [('background', '/home1/h/heqi/cis530/hw2_heqi/models/background.txt.bi.kn.lm'),
                  ('objective', '/home1/h/heqi/cis530/hw2_heqi/models/objective.txt.bi.kn.lm'),
                  ('methods', '/home1/h/heqi/cis530/hw2_heqi/models/methods.txt.bi.kn.lm'),
                  ('results', '/home1/h/heqi/cis530/hw2_heqi/models/results.txt.bi.kn.lm'),
                  ('conclusions', '/home1/h/heqi/cis530/hw2_heqi/models/conclusions.txt.bi.kn.lm')]
    lm_predict(model_list, '/home1/c/cis530/hw2/data/test/excerpts.txt', os.getcwd() + '/hw2_3_1.txt')
    accuracy, bigram_kn_cm = evaluate('/home1/c/cis530/hw2/data/test/labels_all.txt', os.getcwd() + '/hw2_3_1.txt')
    accuracy_list.append(('bi.kn.lm', accuracy))

    # 1.2 write bigram KN confusion table
    fout = open('confusionMatrix.txt', 'w')
    for rows in bigram_kn_cm:
        for i in range(len(rows) - 1):
            fout.write(str(round(rows[i], 2)) + ", ")
        fout.write(str(round(rows[-1], 2)) + '\n')
    fout.close()

    # 2 bigram with add 0.25 smoothing
    model_list = [('background', '/home1/h/heqi/cis530/hw2_heqi/models/background.txt.bi.lm'),
                  ('objective', '/home1/h/heqi/cis530/hw2_heqi/models/objective.txt.bi.lm'),
                  ('methods', '/home1/h/heqi/cis530/hw2_heqi/models/methods.txt.bi.lm'),
                  ('results', '/home1/h/heqi/cis530/hw2_heqi/models/results.txt.bi.lm'),
                  ('conclusions', '/home1/h/heqi/cis530/hw2_heqi/models/conclusions.txt.bi.lm')]
    lm_predict(model_list, '/home1/c/cis530/hw2/data/test/excerpts.txt', os.getcwd() + '/bigram_add.txt')
    accuracy, bigram_kn_cm = evaluate('/home1/c/cis530/hw2/data/test/labels_all.txt', os.getcwd() + '/bigram_add.txt')
    accuracy_list.append(('bi.lm', accuracy))

    # 3 unigram with add 0.25 smoothing
    model_list = [('background', '/home1/h/heqi/cis530/hw2_heqi/models/background.txt.uni.lm'),
                  ('objective', '/home1/h/heqi/cis530/hw2_heqi/models/objective.txt.uni.lm'),
                  ('methods', '/home1/h/heqi/cis530/hw2_heqi/models/methods.txt.uni.lm'),
                  ('results', '/home1/h/heqi/cis530/hw2_heqi/models/results.txt.uni.lm'),
                  ('conclusions', '/home1/h/heqi/cis530/hw2_heqi/models/conclusions.txt.uni.lm')]
    lm_predict(model_list, '/home1/c/cis530/hw2/data/test/excerpts.txt', os.getcwd() + '/unigram_add.txt')
    accuracy, bigram_kn_cm = evaluate('/home1/c/cis530/hw2/data/test/labels_all.txt', os.getcwd() + '/unigram_add.txt')
    accuracy_list.append(('uni.lm', accuracy))

    # 4 write models by accuracy
    sorted_list = sorted(accuracy_list, key=operator.itemgetter(1), reverse=True)
    result_file = open('hw2_3_4.txt', 'w')
    for model_name, values in sorted_list:
        result_file.write(model_name + ' ')
        result_file.write(str(round(values, 2)) + '\n')
    result_file.close()
