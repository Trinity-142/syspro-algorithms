from typing import List

import pytest

class Representative:
    def __init__(self, number, size, left):
        self.number = number
        self.size = size
        self.left = left

class UnionFind:
    def __init__(self, n):
        self.parents = [Representative(i, 1, i) for i in range(n + 1)]

    def find(self, x: int) -> Representative:
        if self.parents[x].number == x: return self.parents[x]
        new_parent = self.find(self.parents[x].number)
        self.parents[x] = new_parent
        return new_parent

    def union(self, x, y):
        x_repr = self.find(x)
        y_repr = self.find(y)

        if x_repr.number == y_repr.number: return

        parent, child = (x_repr, y_repr) if x_repr.size >= y_repr.size else (y_repr, x_repr)
        parent.size += child.size
        parent.left = min(parent.left, child.left)
        self.parents[child.number] = parent

class Task:
    def __init__(self, number, deadline, penalty):
        self.number = number
        self.deadline = deadline
        self.penalty = penalty

    def __repr__(self):
        return f'({self.number}, {self.deadline}, {self.penalty})'

def solution(tasks: List[Task]):
    n = len(tasks)
    schedule = [0] * (n + 1)
    unionfind = UnionFind(n)
    overdue = 0
    while tasks:
        task = tasks.pop()
        if schedule[task.deadline] == 0:
            schedule_index = task.deadline
        else:
            schedule_index = unionfind.find(task.deadline).left
            if schedule_index == 0:
                schedule_index = unionfind.find(n).left
        if schedule_index > task.deadline:
            overdue += 1

        schedule[schedule_index] = task.number
        unionfind.union(schedule_index, schedule_index - 1)

    return schedule[1:], overdue

def naive_greedy(tasks: List[Task]):
    schedule = [0] * (len(tasks) + 1)
    overdue = 0
    for i in range(1, len(tasks) + 1):
        task = tasks.pop()
        schedule[i] = task.number
        if task.deadline < i:
            overdue += 1

    return schedule[1:], overdue

@pytest.mark.parametrize("tasks, optimal_schedule, optimal_overdue", [
        ([Task(2, 4, 10),
          Task(5, 3, 20),
          Task(1, 3, 25),
          Task(3, 1, 30),
          Task(4, 3, 50)],
         [3, 1, 4, 2, 5], 1),
        ([Task(2, 4, 10),
          Task(5, 4, 20),
          Task(1, 4, 25),
          Task(3, 4, 30),
          Task(4, 4, 50)],
         [5, 1, 3, 4, 2], 1),
        ([Task(2, 3, 10),
          Task(5, 2, 20),
          Task(1, 1, 25),
          Task(3, 5, 30),
          Task(4, 5, 50)],
         [1, 5, 2, 3, 4], 0),
        ([Task(2, 4, 10),
          Task(5, 3, 20),
          Task(1, 2, 25),
          Task(3, 1, 30),
          Task(4, 5, 50)],
         [3, 1, 5, 2, 4], 0),
])

def test_solution(tasks, optimal_schedule, optimal_overdue):
    actual_schedule, actual_overdue = solution(tasks.copy())
    assert (actual_schedule == optimal_schedule and actual_overdue == optimal_overdue)
    naive_schedule, naive_overdue = naive_greedy(tasks.copy())
    print("\nTasks: ", tasks)
    print(f"Optimal schedule and overdue:      {optimal_schedule} | {optimal_overdue}")
    print(f"Naive greedy schedule and overdue: {naive_schedule} | {naive_overdue}")
