import string
import time
import random

from benchmarks import format_table

def merge(arr, start, mid, end, buf):
    i = start
    j = mid
    k = start
    while i < mid and j < end:
        if arr[i] < arr[j]:
            buf[k] = arr[i]
            i += 1
        else:
            buf[k] = arr[j]
            j += 1
        k += 1
    while i < mid:
        buf[k] = arr[i]
        i += 1
        k += 1
    while j < end:
        buf[k] = arr[j]
        j += 1
        k += 1

def merge_sort_impl(arr, start, end, buf):
    if end - start <= 1: return
    mid = (start + end) // 2
    merge_sort_impl(arr, start, mid, buf)
    merge_sort_impl(arr, mid, end, buf)

    merge(arr, start, mid, end, buf)
    for i in range(start, end):
        arr[i] = buf[i]

def merge_sort(arr: list) -> list:
    buf = [0] * len(arr)
    merge_sort_impl(arr, 0, len(arr), buf)
    return arr


def radix_sort(a: list[str]) -> list[str]:
    ans = [""] * len(a)
    for n in range(len(a[0]) - 1, -1, -1):
        buf = [0] * (ord(max(a, key=lambda string: string[n])[n])+1)
        for string in a:
            buf[ord(string[n])] += 1
        for i in range(1, len(buf)):
            buf[i] += buf[i-1]
        for i in range(len(a)-1, -1, -1):
            ans[buf[ord(a[i][n])]-1] = a[i]
            buf[ord(a[i][n])] -= 1
        a = ans.copy()
    return a

def generate_test(count, size):
    return [''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)) for _ in range(count)]
tests = []
for n in [1000, 5000, 10000]:
    tests.append(generate_test(10, n))

results = []
print(radix_sort(tests[0]) == merge_sort(tests[0]))
for algo in [radix_sort, merge_sort]:
    curr = []
    for test in tests:
        start = time.time()
        algo(test)
        end = time.time()
        curr.append(round(end - start, 10))
    results.append(curr)

format_table(["Radix sort", "Merge sort"], ["1k Strings len", "5k Strings len", "10k Strings len"], results)