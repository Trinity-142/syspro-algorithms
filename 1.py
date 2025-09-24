import pytest


def divide(a: int, b: int) -> int:
    if a < b:
        return 0
    a = list(map(int, str(a)))
    n = len(a)
    carry = 0
    res = ""
    for i in range(n):
        digit = 0
        curr = carry * 10 + a[i]  # 2 операции
        # итераций цикла от 0 до 9
        while curr >= b:  # 1 операция сравнения
            curr -= b  # операция вычитания m-значного числа, примерно m элементарный операций
            digit += 1  # 1 операция
        carry = curr
        res += str(digit)
    if len(res) > 1:
        res.lstrip("0")
    return int(res)
    # в итоге в лучшем случае примерно O(1) (если a < b)
    # в худшем случае примерно n*(2+9*(1+m+1)) = O(n*m) (если все цифры a = 9, b = 1)


@pytest.mark.parametrize("dividend, divisor, quotient", [(101, 2, 50),
                                                         (645, 3, 215),
                                                         (7, 35, 0),
                                                         (0, 100, 0),
                                                         (51, 25, 2),
                                                         (44, 44, 1)])
def test(dividend, divisor, quotient):
    assert divide(dividend, divisor) == quotient
