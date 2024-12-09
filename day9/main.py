#!/usr/bin/env python3

import itertools
from dataclasses import dataclass


@dataclass
class Span:
    f_id: int | None


def parse_diskmap(diskmap):
    empty = False
    f_id = 0
    res = []
    for s in diskmap:
        l = int(s)
        if empty:
            res.extend([*itertools.repeat(None, l)])
        else:
            res.extend([*itertools.repeat(f_id, l)])
            f_id += 1
        empty = not empty
    return res


def defrag(layout):
    front = 0
    back = len(layout) - 1

    while front < back:
        if layout[front] is not None:
            front += 1
        if layout[back] is None:
            back -= 1
        if layout[front] is None and layout[back] is not None:
            layout[front] = layout[back]
            layout[back] = None


def checksum(defragged):
    return sum(
        pos * f_id
        for pos, f_id in enumerate(
            itertools.takewhile(lambda b: b is not None, defragged)
        )
    )


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    diskmap = lines[0]
    layout = parse_diskmap(diskmap)
    defrag(layout)
    print(checksum(layout))
