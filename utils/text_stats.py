import collections

import sys
sys.path.insert(0, '..')
from utils.int_to_text import num2text


def get_word_pool(numbers): 
    numbers_text = [num2text(num) for num in numbers]
    return [w for s in numbers_text for w in s.split(' ')]


def get_word_counter(numbers):
    counter = collections.Counter()
    for word in get_word_pool(numbers):
        counter[word] += 1
    return counter

    
def get_char_counter(numbers):
    counter = collections.Counter()
    for char in [c for w in get_word_pool(numbers) for c in w]:
        counter[char] += 1
    return counter
    
    
def get_digit_counter(numbers):
    counter = collections.Counter()
    numbers_str = [str(num) for num in numbers]
    for digit in [d for s in numbers_str for d in s]:
        counter[digit] += 1
    return counter

    
def get_length_counter(numbers):
    counter = collections.Counter()
    numbers_str = [str(num) for num in numbers]
    for num_str in numbers_str:
        counter[len(num_str)] += 1
    return counter