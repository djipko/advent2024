#!/usr/bin/env python3
import heapq
import math


def is_valid(x, y, w, h, grid):
    return 0 <= x < w and 0 <= y < h and (x, y) not in grid


def next_step(x, y, w, h, grid):
    for mx, my in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        xx, yy = x + mx, y + my
        if is_valid(xx, yy, w, h, grid):
            yield (xx, yy)


def dijkstra(start, w, h, grid):
    unvisited = set((x, y) for x in range(w) for y in range(h) if (x, y) not in grid)
    shortest = {c: math.inf for c in unvisited}
    frontier = []
    shortest[start] = 0
    heapq.heappush(frontier, (0, start))
    while unvisited and frontier:
        _dist, current_min = heapq.heappop(frontier)

        for nx, ny in next_step(*current_min, w, h, grid):
            if (nx, ny) not in unvisited:
                continue
            tentative = shortest[current_min] + 1
            if tentative < shortest[(nx, ny)]:
                shortest[(nx, ny)] = tentative
                heapq.heappush(frontier, (tentative, (nx, ny)))
        unvisited.discard(current_min)
    return shortest


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    grid = {tuple(map(int, line.split(","))) for line in lines[:1024] if line}
    w, h = 71, 71
    dist = dijkstra((0, 0), w, h, grid)
    print(dist[(w - 1, h - 1)])
    for coord in lines[1024:]:
        c = tuple(map(int, coord.split(",")))
        grid.add(c)
        dist = dijkstra((0, 0), w, h, grid)
        if dist[(w - 1, h - 1)] == math.inf:
            print(",".join(map(str, c)))
            break
