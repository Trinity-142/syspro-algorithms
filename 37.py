from itertools import permutations
from math import factorial

import pytest


def count_topsorts_brute(tree):
    n = len(tree)
    edges = [(u, v) for u in range(n) for v in tree[u]]
    count = 0

    for perm in permutations(range(n)):
        topsort = [0] * n
        for i, v in enumerate(perm):
            topsort[i] = v
        if all(topsort[u] < topsort[v] for u, v in edges):
            count += 1

    return count


def count_topsorts_dp1(tree):
    n = len(tree)
    prev = [0] * n
    for u in range(n):
        for v in tree[u]:
            prev[v] |= 1 << u

    masks = 1 << n
    dp = [0] * masks
    dp[0] = 1

    for mask in range(masks):
        for v in range(n):
            if (mask & (1 << v)) == 0 and (mask & prev[v]) == prev[v]:
                dp[mask | (1 << v)] += dp[mask]

    return dp[masks - 1]


def count_topsorts_dp2(tree):
    n = len(tree)
    size = [0] * n
    dp = [0] * n

    def dfs(u):
        size[u] = 1
        dp[u] = 1
        a = 1
        b = 1
        for v in tree[u]:
            dfs(v)
            size[u] += size[v]
            a *= factorial(size[v])
            b *= dp[v]
        dp[u] = factorial(size[u] - 1) * b // a

    dfs(0)

    return dp[0]


@pytest.mark.parametrize("adj_list", [
    ({0: []}),
    ({0: [1], 1: []}),
    ({0: [1, 2, 3], 1: [], 2: [], 3: []}),
    ({0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}),
    ({0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [], 4: [], 5: [], 6: []}),
    ({0: [1], 1: [2, 3], 2: [4, 5], 3: [6], 4: [], 5: [], 6: []}),
    ({0: [1], 1: [2, 3], 2: [4], 3: [5, 6], 4: [], 5: [], 6: []}),
    ({0: [1, 2], 1: [3, 4], 2: [5], 3: [6], 4: [], 5: [], 6: []}),
    ({0: [1, 2], 1: [3, 4], 2: [5, 6], 3: [], 4: [], 5: [], 6: []}),
    ({0: [1], 1: [2, 7], 2: [3, 8], 3: [4, 9], 4: [5, 10], 5: [6], 6: [], 7: [], 8: [], 9: [], 10: []}),
    ({0: [1, 2, 3], 1: [4, 5], 2: [6], 3: [7, 8, 9], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}),
])
def test_topological_sorts_complex(adj_list):
    result = count_topsorts_dp2(adj_list)
    expected = count_topsorts_dp1(adj_list)
    assert result == expected
