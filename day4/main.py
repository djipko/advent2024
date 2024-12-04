#!/usr/bin/env python3
import itertools

directions = [dir for dir in itertools.product((-1, 0, 1), repeat=2) if dir != (0, 0)]
diags = list(itertools.product((-1, 1), repeat=2))

if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]

    h = len(lines)
    w = len(lines[0])

    def is_valid(c):
        return 0 <= c[0] < w and 0 <= c[1] < h

    def get_next_c(c, d):
        return (c[0] + d[0], c[1] + d[1])

    def match(dir, c, word):
        x, y = c
        if not is_valid(c):
            return False
        nxt, *rest = word
        cur_match = lines[y][x] == nxt
        if not rest:
            return cur_match
        return cur_match and match(dir, get_next_c(c, dir), rest)

    def match_all(c):
        return sum(1 if match(direction, c, "XMAS") else 0 for direction in directions)

    def match_mas(c):
        ms = []
        ss = []
        for d in diags:
            nxt_c = get_next_c(c, d)
            if not is_valid(nxt_c):
                return False
            x, y = nxt_c
            if lines[y][x] == "M":
                ms.append(nxt_c)
            if lines[y][x] == "S":
                ss.append(nxt_c)
        if len(ms) == 2 and len(ss) == 2:
            return ms[0][0] == ms[1][0] or ms[0][1] == ms[1][1]
        return False

    Xs = [(x, y) for y in range(h) for x in range(w) if lines[y][x] == "X"]
    print(sum(match_all(X) for X in Xs))
    As = [(x, y) for y in range(h) for x in range(w) if lines[y][x] == "A"]
    print(sum(1 if match_mas(A) else 0 for A in As))
