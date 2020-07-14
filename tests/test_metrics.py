import dataclasses
import numpy as np
import pytest
import typing as tp

from utils.metrics import levenshtein_distance, wer, ser, mean_wer, mean_ser


@dataclasses.dataclass
class Case:
    first: tp.Sequence[str] = ()
    second: tp.Sequence[str] = ()
    reference: tp.Optional[str] = ''
    recognized: tp.Optional[str] = ''
    y_true: tp.Sequence[str] = ()
    y_pred: tp.Sequence[str] = ()
    result: float = 0
    name: tp.Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'answer_for_{}_and_{}'.format(self.first, self.second)


BIG_VALUE = 1000

TEST_CASES_LEV = [
    Case(first=[], second=['a', 'bit', 'of', 'dummy', 'words'], result=5),
    Case(first=[''], second=['a', 'bit', 'of', 'dummy', 'words'], result=5),
    Case(first=['word'], second=['word'], result=0),
    Case(first=['long', 'sequence', 'of', 'numerous', 'test', 'words', 'verifying', 'correctness',
         'of', 'the', 'algorithm'],
         second=['long', 'sequence', 'of', 'numerous', 'test', 'words', 'verifying', 'correctness',
         'of', 'the', 'algorithm'],
         result=0),
    Case(first=['Levenshtein', 'distance'], second=['equals', 'two'], result=2),
    Case(first=['there', 'is', 'one', 'deletion'], second=['here', 'there', 'is', 'one', 'deletion'], result=1),
    Case(first=['here', 'there', 'is', 'also', 'one', 'deletion'],
         second=['here', 'there', 'is', 'also', 'one', 'little', 'deletion'], result=1),
    Case(first=['it', 'is', 'insertion', 'here'], second=['it', 'is', 'here'], result=1),
    Case(first=['this', 'is', 'a', 'changed', 'word'], second=['this', 'is', 'a', 'new', 'word'], result=1),
    Case(first=['this', 'is', 'a', 'mixed', 'example'], second=['this', 'example', 'is', 'mixed'], result=3),
    Case(first=['yet', 'another', 'random', 'example'],
         second=['just', 'now', 'changed', 'random', 'longer', 'example'], result=4),
    Case(first=['пример', 'на', 'русском', 'языке'],
         second=['чуточку', 'измененный', 'примерчик', 'не', 'на', 'английском', 'языке'], result=5),
    Case(first=['слово'] * BIG_VALUE, second=['слово'] * BIG_VALUE, result=0),
]

TEST_CASES_WER = [
    Case(reference='a bit of dummy words', recognized='', result=1),
    Case(reference='word', recognized='word', result=0),
    Case(reference='long sequence of numerous test words verifying correctness of the algorithm',
         recognized='long sequence of numerous test words verifying correctness of the algorithm',
         result=0),
    Case(reference='equals two', recognized='Levenshtein distance', result=1),
    Case(reference='here there is one deletion', recognized='there is one deletion', result=0.2),
    Case(reference='here there is also one little deletion', recognized='here there is also one deletion',
         result=0.14285714285714285),
    Case(reference='it is here', recognized='it is insertion here', result=0.3333333333333333),
    Case(reference='this is a new word', recognized='this is a changed word', result=0.2),
    Case(reference='this example is mixed', recognized='this is a mixed example', result=0.75),
    Case(reference='just now changed random longer example', recognized='yet another random example',
         result=0.6666666666666666),
    Case(reference='чуточку измененный примерчик не на английском языке', recognized='пример на русском языке',
         result=0.7142857142857143),
    Case(reference='слово ' * BIG_VALUE, recognized='слово ' * BIG_VALUE, result=0),
]

TEST_CASES_SER = [
    Case(reference='dummy string', recognized='', result=1),
    Case(reference='word', recognized='word', result=0),
    Case(reference='puppy', recognized='kitten', result=1.2),
    Case(reference='world', recognized='word', result=0.2),
    Case(reference='word', recognized='world', result=0.25),
    Case(reference='bord', recognized='word', result=0.25),
    Case(reference='строчка', recognized='строка', result=0.14285714285714285),
    Case(reference='s' * BIG_VALUE, recognized='s' * BIG_VALUE, result=0),
]

TEST_CASES_MEAN = [
    Case(y_true=np.array(['a', 'b', 'c']), y_pred=np.array(['a', 'b', 'c']), result=0),
    Case(y_true=np.array(['a', 'b', 'c']), y_pred=np.array(['a', 'd', 'c']), result=0.3333333333333333),
    Case(y_true=np.array(['kitten'] * BIG_VALUE), y_pred=np.array(['puppy'] * BIG_VALUE), result=1),
]


@pytest.mark.parametrize('t', TEST_CASES_LEV, ids=str)
def test_lev(t: Case) -> None:
    answer = levenshtein_distance(t.first, t.second)
    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES_WER, ids=str)
def test_wer(t: Case) -> None:
    answer = wer(t.reference, t.recognized)
    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES_SER, ids=str)
def test_wer(t: Case) -> None:
    answer = ser(t.reference, t.recognized)
    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES_MEAN, ids=str)
def test_wer(t: Case) -> None:
    answer_wer = mean_wer(t.y_true, t.y_pred)
    answer_ser = mean_ser(t.y_true, t.y_pred)
    assert answer_wer == t.result
    assert answer_ser == t.result


def test_empty_reference_assert() -> None:
    with pytest.raises(AssertionError, match='Reference should be non-empty'):
        wer(' ', 'распознанные слова')
    with pytest.raises(AssertionError, match='Reference should be non-empty'):
        ser('', 'распознанная строка')


def test_different_length() -> None:
    with pytest.raises(AssertionError, match='y_true and y_pred should have the same length'):
        mean_wer(np.array(['a', 'b', 'c']), np.array(['a', 'b']))
    with pytest.raises(AssertionError, match='y_true and y_pred should have the same length'):
        mean_ser(np.array(['a', 'b', 'c']), np.array(['a', 'b']))
