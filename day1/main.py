#!/usr/bin/env python3

from collections import Counter

if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    first, second = [], []
    for fst, snd in (line.split() for line in lines if line):
        first.append(int(fst))
        second.append(int(snd))

    print(sum(abs(fst - snd) for fst, snd in zip(sorted(first), sorted(second))))
    second_c = Counter(second)
    print(sum(n * second_c[n] for n in first))
