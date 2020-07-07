import dataclasses
import pytest
import typing as tp

from utils.wer import levenshtein_distance, wer


@dataclasses.dataclass
class Case:
    first: tp.Sequence[str] = ()
    second: tp.Sequence[str] = ()
    recognized: tp.Optional[str] = ''
    reference: tp.Optional[str] = ''
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
    Case(recognized='', reference='a bit of dummy words', result=1),
    Case(recognized='word', reference='word', result=0),
    Case(recognized='long sequence of numerous test words verifying correctness of the algorithm',
         reference='long sequence of numerous test words verifying correctness of the algorithm',
         result=0),
    Case(recognized='Levenshtein distance', reference='equals two', result=1),
    Case(recognized='there is one deletion', reference='here there is one deletion', result=0.2),
    Case(recognized='here there is also one deletion', reference='here there is also one little deletion',
         result=0.14285714285714285),
    Case(recognized='it is insertion here', reference='it is here', result=0.3333333333333333),
    Case(recognized='this is a changed word', reference='this is a new word', result=0.2),
    Case(recognized='this is a mixed example', reference='this example is mixed', result=0.75),
    Case(recognized='yet another random example', reference='just now changed random longer example',
         result=0.6666666666666666),
    Case(recognized='пример на русском языке', reference='чуточку измененный примерчик не на английском языке',
         result=0.7142857142857143),
    Case(recognized='слово ' * BIG_VALUE, reference='слово ' * BIG_VALUE, result=0),
]


@pytest.mark.parametrize('t', TEST_CASES_LEV, ids=str)
def test_lev(t: Case) -> None:
    answer = levenshtein_distance(t.first, t.second)
    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES_WER, ids=str)
def test_wer(t: Case) -> None:
    answer = wer(t.recognized, t.reference)
    assert answer == t.result


def test_empty_reference_assert() -> None:
    with pytest.raises(AssertionError, match='Reference should be non-empty'):
        wer('распознанные слова', ' ')
