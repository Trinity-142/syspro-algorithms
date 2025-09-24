from random import randint
from typing import List
import pytest

def partition(array: List[int], pivot: int) -> int:
    array[pivot], array[0] = array[0], array[pivot]
    pivot = array[0]
    i = 1
    j = len(array) - 1
    while i <= j:
        while i <= j and array[i] < pivot:
            i += 1
        while i <= j and array[j] > pivot:
            j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    array[0], array[j] = array[j], array[0]
    return j

def kth(array: List[int], k: int) -> int:
    if len(array) == 1: return array[0]

    pivot = randint(0, len(array) - 1)
    p = partition(array, pivot)

    if p + 1 == k:
        return array[p]
    elif p + 1 > k:
        return kth(array[:p], k)
    else:
        return kth(array[p + 1:], k - p - 1)

def find_pipeline(input):
    Y = [i[1] for i in input]
    N = len(Y)
    if N % 2 != 0:
        return kth(Y, N // 2 + 1)
    else:
        return (kth(Y, N // 2) + kth(Y, (N // 2) + 1)) / 2

@pytest.mark.parametrize("input, expected", [
    ([(5, 6), (1, 2), (3, 4)], 4),
    ([(2, 3), (1, 2), (3, 4), (0, 1)], 2.5),
    ([(4, 5), (2, -5), (5, 10), (3, 0), (1, -10)], 0),
    ([(5, 10), (6, 15), (1, 3), (3, 6), (2, 3), (4, 8)], 7),
    ([(4, 0), (6, 2), (1, -3), (3, -1), (5, 1), (2, -2), (7, 3)], 0),
    ([(7, 70), (5, 50), (3, 30), (1, 10), (8, 80), (2, 20), (4, 40), (6, 60)], 45),
    ([(3, 30), (-5, -50), (-1, -10), (-2, -20), (1, 10), (-3, -30), (2, 20), (0, 0), (-4, -40)], -10),
    ([(10, 10), (4, 4), (7, 7), (2, 2), (1, 1), (8, 8), (6, 6), (3, 3), (9, 9), (5, 5)], 5.5),
    ([(50, 500), (10, 100), (40, 400), (30, 300), (20, 200)], 300),
    ([(5, 50), (10, 100), (-5, -50), (-10, -100), (15, 150), (0, 0)], 25)
])

def test_find_pipeline_position(input, expected):
    assert find_pipeline(input) == expected