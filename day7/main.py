#!/usr/bin/env python3

import more_itertools


def equation(ops):
    if not ops:
        return
    fst, *rest = ops
    if not rest:
        yield fst
    for oper in ("*", "+"):
        for res in equation(rest):
            match oper:
                case "*":
                    yield int(fst) * int(res)
                case "+":
                    yield int(fst) + int(res)


def equation2(ops):
    if not ops:
        return
    fst, *rest = ops
    if not rest:
        yield fst
    for oper in ("*", "+", "||"):
        for res in equation2(rest):
            match oper:
                case "||":
                    yield int(f"{res}{fst}")
                case "*":
                    yield int(fst) * int(res)
                case "+":
                    yield int(fst) + int(res)


# This was not the correct way as we need to merge with the result
def iter_merges(ops):
    prevs = []
    for idx, (fst, snd) in enumerate(more_itertools.windowed(ops, 2), start=1):
        yield (*prevs, f"{fst}{snd}", *ops[idx + 1 :])
        prevs.append(fst)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]

    s = 0
    hits = set()
    for idx, line in enumerate(lines):
        res, ops_s = line.split(":")
        ops = ops_s.split()
        if int(res) in set(equation(reversed(ops))):
            s += int(res)
            hits.add(idx)
    print(s)
    ss = 0
    for idx, line in enumerate(lines):
        if idx in hits:
            continue
        res, ops_s = line.split(":")
        ops = ops_s.split()
        if int(res) in set(equation2(reversed(ops))):
            ss += int(res)
    print(ss + s)
