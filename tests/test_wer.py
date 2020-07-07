import dataclasses
import pytest
import typing as tp

from utils.wer import levenshtein_distance, wer


@dataclasses.dataclass
class Case:
    first: tp.Sequence[str]
    second: tp.Sequence[str]
    result: float
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
    Case(first=['there', 'is', 'one', 'insertion'], second=['here', 'there', 'is', 'one', 'insertion'], result=1),
    Case(first=['here', 'there', 'is', 'also', 'one', 'insertion'],
         second=['here', 'there', 'is', 'also', 'one', 'little', 'insertion'], result=1),
    Case(first=['it', 'is', 'deletion', 'here'], second=['it', 'is', 'here'], result=1),
    Case(first=['this', 'is', 'a', 'changed', 'word'], second=['this', 'is', 'a', 'new', 'word'], result=1),
    Case(first=['this', 'is', 'a', 'mixed', 'example'], second=['this', 'example', 'is', 'mixed'], result=3),
    Case(first=['yet', 'another', 'random', 'example'],
         second=['just', 'now', 'changed', 'random', 'longer', 'example'], result=4),
    Case(first=['пример', 'на', 'русском', 'языке'],
         second=['чуточку', 'измененный', 'примерчик', 'не', 'на', 'английском', 'языке'], result=5),
    Case(first=['слово'] * BIG_VALUE, second=['слово'] * BIG_VALUE, result=0),
]

TEST_CASES_WER = [
    Case(first='', second='a bit of dummy words', result=1),
    Case(first='word', second='word', result=0),
    Case(first='long sequence of numerous test words verifying correctness of the algorithm',
         second='long sequence of numerous test words verifying correctness of the algorithm',
         result=0),
    Case(first='Levenshtein distance', second='equals two', result=1),
    Case(first='there is one insertion', second='here there is one insertion', result=0.2),
    Case(first='here there is also one insertion', second='here there is also one little insertion',
         result=0.14285714285714285),
    Case(first='it is deletion here', second='it is here', result=0.3333333333333333),
    Case(first='this is a changed word', second='this is a new word', result=0.2),
    Case(first='this is a mixed example', second='this example is mixed', result=0.75),
    Case(first='yet another random example', second='just now changed random longer example',
         result=0.6666666666666666),
    Case(first='пример на русском языке', second='чуточку измененный примерчик не на английском языке',
         result=0.7142857142857143),
    Case(first='слово ' * BIG_VALUE, second='слово ' * BIG_VALUE, result=0),
]


@pytest.mark.parametrize('t', TEST_CASES_LEV, ids=str)
def test_lev(t: Case) -> None:
    answer = levenshtein_distance(t.first, t.second)
    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES_WER, ids=str)
def test_wer(t: Case) -> None:
    answer = wer(t.first, t.second)
    assert answer == t.result


def test_empty_reference_assert() -> None:
    with pytest.raises(AssertionError, match='Reference should be non-empty'):
        wer('распознанные слова', ' ')
