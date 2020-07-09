# -*- coding: utf-8 -*-
import pytest

from utils.int_to_text import num2text

TEST_CASES_NUMS2TEXT = [
    {'num':0, 'result':'ноль'},
    {'num':5, 'result':'пять'},
    {'num':22, 'result':'двадцать два'},
    {'num':333, 'result':'триста тридцать три'},
    {'num':100243, 'result':'сто тысяч двести сорок три'},
    {'num':1000000, 'result':'один миллион'},
    {'num':-1, 'result':'минус один'}
]

@pytest.mark.int_to_text
@pytest.mark.parametrize('case', TEST_CASES_NUMS2TEXT)
def test_num2text(case):
    assert num2text(case['num']) == case['result'] 
