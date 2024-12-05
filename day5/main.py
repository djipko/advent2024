#!/usr/bin/env python3
from collections import defaultdict
import functools


@functools.total_ordering
class Page:
    def __init__(self, num, topo):
        self.num = num
        self.topo = topo

    def __lt__(self, other):
        return other.num in self.topo.get(self.num, set())

    def __eq__(self, other):
        return self.num == other.num

    def __repr__(self):
        return f"<P {self.num}>"


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data

    topo: dict[str, set[str]] = defaultdict(set)
    updates = list()

    for line in lines:
        if "|" in line:
            fst, snd = line.split("|")
            topo[fst].add(snd)
        elif "," in line:
            updates.append([Page(num, topo) for num in line.split(",")])

    s = 0
    s2 = 0
    sorted_updates = [sorted(update) for update in updates]
    for update, s_update in zip(updates, sorted_updates):
        if update == s_update:
            s += int(update[len(update) // 2].num)
        else:
            s2 += int(s_update[len(s_update) // 2].num)

    print(s)
    print(s2)
