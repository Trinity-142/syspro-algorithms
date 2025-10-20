from __future__ import annotations
import random
from typing import Tuple, List, Optional
import pytest


class ImplicitTreapNode:
    def __init__(self, value):
        self.value = value
        self.priority = random.random()
        self.size = 1
        self.sum = value
        self.left = None
        self.right = None


class ImplicitTreap:
    def __init__(self, root: ImplicitTreapNode = None):
        self.root = root

    def _update(self, node: ImplicitTreapNode):
        if node is None:
            return

        node.size = 1
        node.sum = node.value
        if node.left is not None:
            node.size += node.left.size
            node.sum += node.left.sum
        if node.right is not None:
            node.size += node.right.size
            node.sum += node.right.sum

    def _split_by_size(self, node: ImplicitTreapNode, key: int) -> Tuple[Optional[ImplicitTreapNode], Optional[ImplicitTreapNode]]:
        if node is None:
            return None, None

        left_size = node.left.size if node.left else 0
        if key <= left_size:
            left, node.left = self._split_by_size(node.left, key)
            self._update(node)
            return left, node
        else:
            node.right, right = self._split_by_size(node.right, key - left_size - 1)
            self._update(node)
            return node, right

    def merge(self, left: ImplicitTreapNode, right: ImplicitTreapNode) -> ImplicitTreapNode:
        if left is None:
            return right
        if right is None:
            return left

        if left.priority < right.priority:
            left.right = self.merge(left.right, right)
            self._update(left)
            return left
        else:
            right.left = self.merge(left, right.left)
            self._update(right)
            return right

    def sum(self, from_idx: int, to_idx: int) -> int:
        left, temp = self._split_by_size(self.root, from_idx)
        mid, right = self._split_by_size(temp, to_idx - from_idx + 1)
        result = mid.sum if mid else 0
        temp = self.merge(mid, right)
        self.root = self.merge(left, temp)
        return result

    def build_from_array(self, arr: List[int]):
        self.root = ImplicitTreapNode(arr[0])
        for i in range(1, len(arr)):
            self.root = self.merge(self.root, ImplicitTreapNode(arr[i]))


@pytest.mark.parametrize("arr, from_idx, to_idx, expected_sum",
                         [([1, 2, 3, 4, 5], 0, 4, 15),
                          ([1, 2, 3, 4, 5], 1, 3, 9),
                          ([1, 2, 3, 4, 5], 0, 0, 1),
                          ([-1, 2, -3, 4, -5], 0, 4, -3),
                          (list(range(1, 11)), 0, 9, 55)])
def test_sum_range(arr, from_idx, to_idx, expected_sum):
    treap = ImplicitTreap()
    treap.build_from_array(arr)
    assert treap.sum(from_idx, to_idx) == expected_sum
