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


def calculate_precision_recall_f1score(confusion_matrix: list) -> dict:
    """

    :param confusion_matrix:
    :return:
    """
    scores = {}
    classes = ['N', 'R', 'S']

    for i in range(3):
        precision = confusion_matrix[i][i] / sum(confusion_matrix[i])
        recall = confusion_matrix[i][i] / sum([confusion_matrix[j][i] for j in range(3)])
        f1score = (2 * precision * recall) / (precision + recall)
        scores[classes[i]] = {'precision': precision, 'recall': recall, 'f1score':f1score}

    return scores


for i in range(5):
    build_confusion_matrix("test_set_predicted_output_%d" % i, "confusion_matrix_%d" % i)
