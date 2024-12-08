#!/usr/bin/env python3

import itertools
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def valid_for(self, w, h):
        return 0 <= self.x < w and 0 <= self.y < h


def taxicab(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_antinodes(w, h, a1: P, a2: P):
    left, right = (a1, a2) if a1.x < a2.x else (a2, a1)
    left_x = left.x - abs(a1.x - a2.x)
    right_x = right.x + abs(a1.x - a2.x)

    top, bottom = (a1, a2) if a1.y < a2.y else (a2, a1)
    top_y = top.y - abs(a1.y - a2.y)
    bottom_y = bottom.y + abs(a1.y - a2.y)

    top_c = [P(left_x, top_y), P(right_x, top_y)]
    antinode_top = sorted(top_c, key=lambda p: taxicab(p, top))[0]
    if antinode_top.valid_for(w, h):
        yield antinode_top, top
    bottom_c = [P(left_x, bottom_y), P(right_x, bottom_y)]
    antinode_bottom = sorted(bottom_c, key=lambda p: taxicab(p, bottom))[0]
    if antinode_bottom.valid_for(w, h):
        yield antinode_bottom, bottom


def search_antinodes(w, h, a1, a2, visited=None):
    visited = visited or set()
    if frozenset((a1, a2)) in visited:
        return
    pairs = list(get_antinodes(w, h, a1, a2))
    visited.add(frozenset((a1, a2)))
    for pair in pairs:
        yield pair[0]
    for pair in pairs:
        yield from search_antinodes(w, h, *pair, visited=visited)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]
    w = len(lines[0])
    h = len(lines)
    antenas_by_f = defaultdict(list)
    for y in range(h):
        for x in range(w):
            if (f := lines[y][x]) not in "#.":
                antenas_by_f[f].append(P(x, y))
    antinodes = set()
    harmonic_antinodes = set()
    for f, antenas in antenas_by_f.items():
        for a1, a2 in itertools.product(antenas, repeat=2):
            if a1 == a2:
                continue
            antinodes |= set(a[0] for a in get_antinodes(w, h, a1, a2))
            harmonic_antinodes |= set(search_antinodes(w, h, a1, a2))
    all_antenas = set.union(*(set(ant) for ant in antenas_by_f.values()))
    print(len(antinodes))
    print(len(harmonic_antinodes | all_antenas))
