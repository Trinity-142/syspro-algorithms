import math
import random
import sys
from typing import Tuple


class BloomFilter:
    def __init__(self, s, e):
        self.bitset = 0
        self.s = s
        self.e = e
        self.b = math.ceil(math.log(self.e, 1 / 2) / math.log(2))
        self.k = math.ceil(self.b * math.log(2))
        self.n = self.b * self.s
        self.weights = [tuple(random.randint(0, self.n - 1) for _ in range(4)) for _ in range(self.k)]

    def _hash(self, i, ip: Tuple):
        return sum(a * x for a, x in zip(self.weights[i], ip)) % self.n

    def insert(self, ip: Tuple):
        for i in range(self.k):
            hash = self._hash(i, ip)
            self.bitset |= (1 << hash)

    def lookup(self, ip: Tuple) -> bool:
        for i in range(self.k):
            if not self.bitset & (1 << self._hash(i, ip)):
                return False
        return True


if __name__ == '__main__':
    for s, e in [(100, 0.001), (500, 0.003), (1000, 0.008), (100000, 0.012)]:
        fp = 0
        f = BloomFilter(s, e)
        ips = [tuple(random.randint(0, 255) for _ in range(4)) for i in range(s)]
        other_ips = [tuple(random.randint(0, 255) for _ in range(4)) for i in range(s)]
        for ip in ips:
            f.insert(ip)
        for other_ip in other_ips:
            if f.lookup(other_ip) and other_ip not in ips:
                fp += 1

        memory = sys.getsizeof(f.bitset) + sys.getsizeof(f.weights)
        print(f"Percent of FP: {fp / s}%\n"
              f"Memory used: {memory / 1024} KB\n"
              f"---------------------------------")
