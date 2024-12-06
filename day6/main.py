#!/usr/bin/env python3

from collections import deque

directions = "URDL"


class Loop(Exception):
    pass


class Guard:
    def __init__(self, x, y, h, w, obstacles):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.obstacles = obstacles
        self.visited = set()
        self.visited_w_dir = set()
        self.dirs = deque(directions)

    def move(self):
        self.visited.add((self.x, self.y))
        self.visited_w_dir.add(((self.x, self.y), self.dirs[0]))
        x, y = self.x, self.y
        match self.dirs[0]:
            case "L":
                x -= 1
            case "R":
                x += 1
            case "U":
                y -= 1
            case "D":
                y += 1
        if not self.valid(x, y):
            self.visited.add((self.x, self.y))
            return False
        elif ((x, y), self.dirs[0]) in self.visited_w_dir:
            raise Loop()
        elif (x, y) in self.obstacles:
            self.dirs.rotate(-1)
        else:
            self.x, self.y = x, y
        return True

    def valid(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]
    h = len(lines)
    w = len(lines[0])
    obstacles = [(x, y) for y in range(h) for x in range(w) if lines[y][x] == "#"]
    gx, gy = [(x, y) for y in range(h) for x in range(w) if lines[y][x] == "^"][0]
    guard = Guard(gx, gy, h, w, obstacles)
    while guard.move():
        pass
    print(len(guard.visited))
    new_obs = list(guard.visited)
    loops = 0
    for obs in new_obs:
        if obs == (gx, gy):
            continue
        obs_mod = set([*obstacles, obs])
        guard = Guard(gx, gy, h, w, obs_mod)
        try:
            while guard.move():
                pass
        except Loop:
            loops += 1
    print(loops)
