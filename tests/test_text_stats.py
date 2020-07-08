import pytest

from utils.text_stats import get_word_counter, get_digit_counter, get_length_counter, get_char_counter


TEST_CASES_WORD = [
    {'input': [1, 2, 3, 41, 33], 'feature': 'один', 'result': 2},
    {'input': [1, 2, 3, 41, 33], 'feature': 'сорок', 'result': 1},
    {'input': [1, 2, 3, 41, 33], 'feature': 'три', 'result': 2},
]

TEST_CASES_DIGIT = [
    {'input': [1, 2, 3, 41, 33], 'feature': '1', 'result': 2},
    {'input': [1, 2, 3, 41, 33], 'feature': '3', 'result': 3},
    {'input': [1, 2, 3, 41, 33], 'feature': '2', 'result': 1},
]

TEST_CASES_CHAR = [
    {'input': [1, 2, 3, 41, 33], 'feature': 'ч', 'result': 0},
    {'input': [1, 2, 3, 41, 33], 'feature': 'т', 'result': 4},
    {'input': [1, 2, 3, 41, 33], 'feature': 'о', 'result': 4},
]

TEST_CASES_LENGTH = [
    {'input': [1, 2, 3, 41, 33], 'feature': 1, 'result': 3},
    {'input': [1, 2, 3, 41, 33], 'feature': 2, 'result': 2},
    {'input': [1, 2, 3, 41, 33], 'feature': 3, 'result': 0},
]



@pytest.mark.text_stats
@pytest.mark.parametrize('case', TEST_CASES_WORD)
def test_word_counter(case):
    assert get_word_counter(case['input'])[case['feature']] == case['result']


@pytest.mark.text_stats
@pytest.mark.parametrize('case', TEST_CASES_DIGIT)
def test_digit_counter(case):
    assert get_digit_counter(case['input'])[case['feature']] == case['result']


@pytest.mark.text_stats
@pytest.mark.parametrize('case', TEST_CASES_CHAR)
def test_char_counter(case):
    assert get_char_counter(case['input'])[case['feature']] == case['result']


@pytest.mark.text_stats
@pytest.mark.parametrize('case', TEST_CASES_LENGTH)
def test_length_counter(case):
    assert get_length_counter(case['input'])[case['feature']] == case['result']