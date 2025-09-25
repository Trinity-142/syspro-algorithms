from typing import List

import pytest


class Representative:
    number = None

    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        return self.number == other.number


class UnionFind:
    def __init__(self, n):
        self.parents: List[Representative] = [0] * (n + 1)
        for i in range(1, n + 1):
            self.parents[i] = Representative(i)

    def find(self, x) -> Representative:
        curr = x
        while self.parents[curr].number != curr:
            curr = self.parents[curr].number

        self.parents[x] = self.parents[curr]
        return self.parents[curr]

    def union(self, x, y):
        x_repr = self.find(x)
        y_repr = self.find(y)
        self.parents[x_repr.number] = y_repr

class Task:
    def __init__(self, number, deadline, penalty):
        self.number = number
        self.deadline = deadline
        self.penalty = penalty

    def __repr__(self):
        return f'({self.number}, {self.deadline}, {self.penalty})'

def solution(tasks: List[Task]):
    schedule = [0] * (len(tasks) + 1)
    unionfind = UnionFind(len(tasks))
    overdue = 0
    while tasks:
        task = tasks.pop()
        if schedule[task.deadline] == 0:
            schedule_index = task.deadline
        else:
            schedule_index = unionfind.find(task.deadline).number

        schedule[schedule_index] = task.number
        if schedule_index > task.deadline:
            overdue += 1
        if schedule_index == 1:
            unionfind.union(schedule_index, schedule_index - 2)
        else:
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
