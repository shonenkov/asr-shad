import Levenshtein
import sklearn.metrics
import typing as tp


def levenshtein_distance(first: tp.Sequence[tp.Any], second: tp.Sequence[tp.Any]) -> int:
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


def wer(reference: str, recognized: str) -> float:
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


def ser(reference: str, recognized: str) -> float:
    """
    Compute symbol error rate between two strings
    :param recognized: recognized string consisting of symbols
    :param reference: correct phrase consisting of positive number of symbols
    :return: symbol error rate
    """
    assert len(reference) > 0, 'Reference should be non-empty'

    return Levenshtein.distance(recognized, reference) / len(reference)


def mean_score(y_true: tp.Sequence[str], y_pred: tp.Sequence[str], kind: str) -> float:
    """
    Compute mean WER or mean SER for two vectors
    :param y_true: vector of true strings
    :param y_pred: vector of predicted strings
    :param kind: kind of error rate to compute, wer for word or ser for symbol error rate
    :return: mean word/symbol error rate
    """
    assert len(y_true) == len(y_pred), 'y_true and y_pred should have the same length'
    assert kind in ['ser', 'wer'], 'Kind should be ser or wer'

    metric = globals()[kind]
    score = 0
    for i in range(len(y_true)):
        score += metric(y_true[i], y_pred[i])
    return score / len(y_true) if len(y_true) else 0


def mean_wer(y_true, y_pred):
    """Compute mean word error rate for two vectors"""
    return mean_score(y_true, y_pred, kind='wer')


def mean_ser(y_true, y_pred):
    """Compute mean symbol error rate for two vectors"""
    return mean_score(y_true, y_pred, kind='ser')


# Transform metrics to sklearn-compatible form
mean_wer_score = sklearn.metrics.make_scorer(mean_wer, greater_is_better=False)
mean_ser_score = sklearn.metrics.make_scorer(mean_ser, greater_is_better=False)
