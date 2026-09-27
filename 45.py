import itertools
import random


def naive_tsp(graph):
    n = len(graph)
    m_path = []
    m = float('inf')
    for p in itertools.permutations(list(range(1, n))):
        path = [0] + list(p) + [0]
        dist = 0
        for i in range(n):
            dist += graph[path[i]][path[i + 1]]
        if dist < m:
            m = dist
            m_path = path
    return m, m_path


def held_karp_tsp(graph):
    n = len(graph)
    A = [[float('inf')] * (1 << n) for _ in range(n)]
    A[0][1] = 0
    for m in range(2, n + 1):
        for s in range(1, 1 << n):
            if s.bit_count() != m or not (s & 1): continue
            for v in range(1, n):
                if not (s >> v) & 1: continue
                min_dist = float('inf')
                for w in range(n):
                    if not (s >> w) & 1 or w == v: continue
                    prev = s ^ (1 << v)
                    cost = A[w][prev] + graph[w][v]
                    if cost < min_dist:
                        min_dist = cost
                A[v][s] = min_dist

    dist = float('inf')
    for v in range(1, n):
        cost = A[v][(1 << n) - 1] + graph[v][0]
        if cost < dist:
            dist = cost
            last = v

    path = [0, last]
    curr_v = last
    curr_s = (1 << n) - 1
    while curr_s != 1:
        prev_s = curr_s ^ (1 << curr_v)
        for w in range(n):
            if (prev_s >> w) & 1:
                if A[curr_v][curr_s] == A[w][prev_s] + graph[w][curr_v]:
                    curr_v = w
                    curr_s = prev_s
                    path.append(w)
                    break

    return dist, path[::-1]


if __name__ == '__main__':
    for n in range(4, 100):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                weight = random.randint(1, 100)
                graph[i][j] = weight
                graph[j][i] = weight
        #dist1, path1 = naive_tsp(graph)
        #dist2, path2 = held_karp_tsp(graph)
        #print(n, held_karp_tsp(graph), naive_tsp(graph), set(path1) == set(path2))
        print(n, held_karp_tsp(graph))
