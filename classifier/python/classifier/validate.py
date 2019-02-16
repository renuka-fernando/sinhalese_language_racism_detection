import logging
import sys

sys.path.append("../")
sys.path.append("../../../sinhala-preprocessing/python")
from classifier.utils import get_last_results_folder


def prediction(n: float, r: float, s: float) -> int:
    """
    Returns label of the class with maximum probability
    :param n: probability of being Neutral
    :param r: probability of being Racist
    :param s: probability of being Sexism
    :return: label of the class with maximum probability
    """
    lst = [n, r, s]
    maximum = max(lst)
    max_index = lst.index(maximum)

    return [0, 1, 2][max_index]


def build_confusion_matrix(result_file_name: str, confusion_matrix_file_name: str) -> list:
    """
    calculate confusion matrix and save to disk
    :param result_file_name: result file to read
    :param confusion_matrix_file_name: file name to save the confusion matrix
    :return: confusion matrix
    """
    file = open(result_file_name, "r")
    lines = file.readlines()
    file.close()

    # confusion matrix
    # .... true class: N, R, S
    predicted_true = [[0, 0, 0],  # N - Predicted class
                      [0, 0, 0],  # R - Predicted class
                      [0, 0, 0]]  # S - Predicted class

    for line in lines:
        tweet_id, label, neutral, racist, sexism = line.strip().split(",")
        predicted_class = prediction(float(neutral), float(racist), float(sexism))
        predicted_true[predicted_class][int(label)] += 1

    file = open(confusion_matrix_file_name, 'w')
    for result_line in predicted_true:
        file.write(",".join([str(result) for result in result_line]) + '\n')
    file.close()

    return predicted_true


def calculate_precision_recall_f1score(confusion_matrix: list, score_file_name: str) -> dict:
    """
    calculate precision, recall and f1 score
    :param confusion_matrix: confusion matrix
    :param score_file_name: file name to save scores
    :return: {precision, recall, f1 score}
    """
    scores = {}
    classes = ['N', 'R', 'S']
    file = open(score_file_name, 'w')

    for i in range(3):
        try:
            precision = round(confusion_matrix[i][i] / sum(confusion_matrix[i]), 4)
        except ZeroDivisionError:
            precision = "INFINITE"

        try:
            recall = round(confusion_matrix[i][i] / sum([confusion_matrix[j][i] for j in range(3)]), 4)
        except ZeroDivisionError:
            recall = "INFINITE"

        if precision != "INFINITE" and recall != "INFINITE":
            try:
                f1score = round((2 * precision * recall) / (precision + recall), 4)
            except ZeroDivisionError:
                f1score = "NaN"
        else:
            f1score = "NaN"

        scores[classes[i]] = {'precision': precision, 'recall': recall, 'f1score': f1score}
        file.write("%s: {precision:%s, recall:%s, f1score:%s}\n" % (classes[i], precision, recall, f1score))

    file.close()
    return scores


logging.basicConfig(format='%(levelname)s %(asctime)s: %(message)s', level=logging.INFO)
directory = get_last_results_folder()
logging.info("Validating on %s" % directory)

for i in range(5):  # here 5 is the number of folds
    matrix = build_confusion_matrix("%s/test_set_predicted_output_%d.txt" % (directory, i),
                                    "%s/confusion_matrix_%d.txt" % (directory, i))
    calculate_precision_recall_f1score(matrix, "%s/scores_%d.txt" % (directory, i))
