import pytest


def karatsuba(first: int, second: int) -> int:
    first, second = str(first), str(second)
    N = max(len(first), len(second))
    if N == 1:
        return int(first) * int(second)
    if N % 2 != 0:
        N += 1
    first = first.zfill(N)
    second = second.zfill(N)
    k = N // 2
    a, b = int(first[:k]), int(first[k:])
    c, d = int(second[:k]), int(second[k:])
    step1 = karatsuba(a, c)
    step2 = karatsuba(b, d)
    step3 = karatsuba((a + b), (c + d))
    step4 = step3 - step2 - step1
    return step1 * 10 ** N + step4 * 10 ** k + step2


@pytest.mark.parametrize("multiplier, multiplicand, product", [(1234, 5678, 7006652),
                                                               (56, 642, 35952),
                                                               (645, 324, 208980),
                                                               (645, 2, 1290),
                                                               (2, 1234543, 2469086),
                                                               (0, 25, 0),
                                                               (25, 0, 0)])
def test(multiplier, multiplicand, product):
    assert karatsuba(multiplier, multiplicand) == product
