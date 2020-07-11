def levenshtein_distance(first, second):
    """
    Compute Levenshtein distance between two array-like objects
    """
    distance = [[0 for _ in range(len(second) + 1)] for _ in range(len(first) + 1)]
    for i in range(len(first) + 1):
        for j in range(len(second) + 1):
            if i == 0:
                distance[i][j] = j
            elif j == 0:
                distance[i][j] = i
            else:
                diag = distance[i - 1][j - 1] + (first[i - 1] != second[j - 1])
                upper = distance[i - 1][j] + 1
                left = distance[i][j - 1] + 1

                distance[i][j] = min(diag, upper, left)

    return distance[len(first)][len(second)]


def wer(recognized, reference):
    """
    Compute world error rate between two phrases
    :param recognized: recognized phrase consisting of words separated with spaces, could be empty
    :param reference: correct phrase consisting of positive number of words separated with spaces
    :return: world error rate
    """
    recognized_sequence = list(recognized.split())
    reference_sequence = list(reference.split())
    assert len(reference_sequence) > 0, 'Reference should be non-empty'

    return levenshtein_distance(recognized_sequence, reference_sequence) / len(reference_sequence)
