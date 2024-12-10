#!/usr/bin/env python3


def is_valid(x, y, w, h):
    return 0 <= x < w and 0 <= y < h


def next_step(x, y, w, h, grid):
    for mx, my in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        xx, yy = x + mx, y + my
        if is_valid(xx, yy, w, h) and grid[yy][xx] == grid[y][x] + 1:
            yield (xx, yy)


def _step_score(sx, sy, w, h, grid, seen_peaks=None):
    if grid[sy][sx] == 9:
        if seen_peaks is not None and (sx, sy) not in seen_peaks:
            seen_peaks.add((sx, sy))
            return 1
        elif seen_peaks is None:
            return 1
        return 0

    return sum(
        _step_score(nx, ny, w, h, grid, seen_peaks)
        for nx, ny in next_step(sx, sy, w, h, grid)
    )


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]
    grid = [[int(x) for x in line] for line in lines]
    # do stuff with data
    w = len(grid[0])
    h = len(grid)
    zeros = [(x, y) for y in range(h) for x in range(w) if grid[y][x] == 0]
    print(sum(_step_score(zx, zy, w, h, grid, set()) for zx, zy in zeros))
    print(sum(_step_score(zx, zy, w, h, grid) for zx, zy in zeros))
