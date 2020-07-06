import dataclasses
import pytest
import typing as tp

from utils.wer import wer


@dataclasses.dataclass
class Case:
    first: tp.AnyStr
    second: tp.AnyStr
    result: float
    name: tp.Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'wer_between_{}_and_{}'.format(self.first, self.second)


BIG_VALUE = 1000

TEST_CASES = [
    Case(first='', second='a bit of dummy words', result=1),
    Case(first='word', second='word', result=0),
    Case(first='long sequence of numerous test words verifying correctness of the algorithm',
         second='long sequence of numerous test words verifying correctness of the algorithm',
         result=0),
    Case(first='Levenshtein distance', second='equals two', result=1),
    Case(first='there is one insertion', second='here there is one insertion', result=1/5),
    Case(first='here there is also one insertion', second='here there is also one little insertion', result=1/7),
    Case(first='it is deletion here', second='it is here', result=1/3),
    Case(first='this is a changed word', second='this is a new word', result=1/5),
    Case(first='this is a mixed example', second='this example is mixed', result=3/4),
    Case(first='yet another random example', second='just now changed random longer example', result=4/6),
    Case(first='пример на русском языке', second='чуточку измененный примерчик не на английском языке', result=5/7),
    Case(first='слово ' * BIG_VALUE, second='слово ' * BIG_VALUE, result=0),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_wer(t: Case) -> None:
    answer = wer(t.first, t.second)
    assert answer == t.result


def test_empty_reference_assert() -> None:
    with pytest.raises(AssertionError, match='Reference should be non-empty'):
        wer('распознанные слова', ' ')
