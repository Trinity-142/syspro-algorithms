from benchmarks import format_table
import numpy as np
import time
import sys

def classic(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    N = len(X)
    res = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            for k in range(N):
                res[i][j] += X[i][k] * Y[k][j]
    return res

def recursive(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    l = X.shape[0]
    if l <= 64:
        return classic(X, Y)
    N = l
    N //= 2
    A, B, C, D = X[:N, :N], X[:N, N:], X[N:, :N], X[N:, N:]
    E, F, G, H = Y[:N, :N], Y[:N, N:], Y[N:, :N], Y[N:, N:]
    top = np.hstack((recursive(A, E) + recursive(B, G), recursive(A, F) + recursive(B, H)))
    bottom = np.hstack((recursive(C, E) + recursive(D, G), recursive(C, F) + recursive(D, H)))
    result = np.vstack((top, bottom))
    return result

def strassen(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    l = X.shape[0]
    if l <= 64:
        return classic(X, Y)
    N = l
    N //= 2
    A, B, C, D = X[:N, :N], X[:N, N:], X[N:, :N], X[N:, N:]
    E, F, G, H = Y[:N, :N], Y[:N, N:], Y[N:, :N], Y[N:, N:]
    P1, P2, P3 = strassen(A, F - H), strassen(A+B, H), strassen(C+D, E)
    P4, P5, P6, P7 = strassen(D, G-E), strassen(A+D, E+H), strassen(B-D, G+H), strassen(A-C, E+F)
    Q1 = P5 + P4 - P2 + P6
    Q2 = P1 + P2
    Q3 = P3 + P4
    Q4 = P1 + P5 - P3 - P7
    top = np.hstack((Q1, Q2))
    bottom = np.hstack((Q3, Q4))
    result = np.vstack((top, bottom))
    return result

def result(func, X, Y):
    res = []
    for _ in range(5):
        start = time.time()
        func(X, Y)
        end = time.time()
        res.append(end - start)
    res = np.array(res)
    sample_mean = round(np.mean(res), 5)
    std = round(np.std(res), 5)
    geometric_mean = round(np.prod(res) ** (1 / res.shape[0]), 5)
    return [sample_mean, std, geometric_mean]

with open("benchmarks.txt", "w") as f:
    start = time.time()
    sys.stdout = f
    for i in [16, 32, 64, 128, 256, 512, 1024]:
        print(f"Matrix size = {i}")
        X = np.random.randint(100, size=(i, i))
        Y = np.random.randint(100, size=(i, i))
        results = [result(classic, X, Y),
                   result(recursive, X, Y),
                   result(strassen, X, Y)]
        format_table(["Classic", "Recursive", "Strassen"], ["Sample mean", "Standard deviation", "Geometric mean"], results)
        print()
        print(time.time() - start, i, file=sys.__stdout__)
    stop = time.time()
    print(f"Total program running time: {stop - start}")