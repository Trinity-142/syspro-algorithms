from typing import List


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


def solution(tasks: List[Task]):
    schedule = [0] * (len(tasks) + 1)
    unionfind = UnionFind(len(tasks))
    while tasks:
        task = tasks.pop()
        if schedule[task.deadline] == 0:
            schedule_index = task.deadline
        else:
            schedule_index = unionfind.find(task.deadline).number

        schedule[schedule_index] = task.number
        if schedule_index == 1:
            unionfind.union(schedule_index, schedule_index - 2)
        else:
            unionfind.union(schedule_index, schedule_index - 1)

    return schedule[1:]

if __name__ == '__main__':
    tasks = [Task(2, 4, 10),
             Task(5, 3, 20),
             Task(1, 3, 25),
             Task(3, 1, 30),
             Task(4, 3, 50)]

    print(solution(tasks))