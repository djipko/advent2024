#!/usr/bin/env python3

import functools
import itertools


def blink(stones):
    new_stones = []
    for stone in stones:
        if stone == "0":
            new_stones.append("1")
        elif (l := len(stone)) % 2 == 0:
            new_stones.append(str(int(stone[: l // 2])))
            new_stones.append(str(int(stone[l // 2 :])))
        else:
            new_stones.append(str(int(stone) * 2024))
    return new_stones


@functools.cache
def blink2(stone, steps):
    if steps == 0:
        return 1
    if stone == "0":
        return blink2("1", steps - 1)
    elif (l := len(stone)) % 2 == 0:
        return blink2(str(int(stone[: l // 2])), steps - 1) + blink2(
            str(int(stone[l // 2 :])), steps - 1
        )
    else:
        new_stone = int(stone)
        for cnt in itertools.count(start=1):
            new_stone = new_stone * 2024
            if len(str(new_stone)) % 2 == 0:
                return blink2(str(new_stone), steps - cnt)
            if cnt == steps:
                return cnt


def do_blink(stones, steps):
    return sum(blink2(stone, steps) for stone in stones)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    stones = lines[0].split()
    print(do_blink(stones, 75))
