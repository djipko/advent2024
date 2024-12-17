#!/usr/bin/env python3

import itertools


def is_valid(x, y, w, h):
    return 0 <= x < w and 0 <= y < h


def next_step(x, y, w, h, grid):
    for mx, my in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        xx, yy = x + mx, y + my
        if is_valid(xx, yy, w, h) and grid[yy][xx] == grid[y][x]:
            yield (xx, yy)


def count_perim(x, y, w, h, grid):
    p = 0
    for mx, my in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        xx, yy = x + mx, y + my
        if (is_valid(xx, yy, w, h) and grid[yy][xx] != grid[y][x]) or not is_valid(
            xx, yy, w, h
        ):
            p += 1
    return p


def find_area(x, y, w, h, grid, area):
    if (x, y) in area:
        return
    area.add((x, y))
    for nx, ny in next_step(x, y, w, h, grid):
        find_area(nx, ny, w, h, grid, area)


def get_price(area, w, h, grid):
    perim = sum(count_perim(x, y, w, h, grid) for x, y in area)
    return perim * len(area)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]
    # do stuff with data
    w = len(lines[0])
    h = len(lines)
    visited = set()
    coords = set(itertools.product(range(w), range(h)))
    areas = []
    while len(visited) < w * h:
        start = next(iter(coords - visited), None)
        if not start:
            break
        area = set()
        find_area(*start, w, h, lines, area)
        visited |= area
        areas.append(area)
    print(sum(get_price(area, w, h, lines) for area in areas))
