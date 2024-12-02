#!/usr/bin/env python3
import more_itertools


def dampened(report):
    for i in range(len(report)):
        yield report[:i] + report[i + 1 :]


def is_safe(report):
    desc = None
    for fst, snd in more_itertools.windowed(report, 2):
        if desc is None:
            desc = fst > snd
        if abs(fst - snd) > 3 or fst == snd:
            return False
        if desc and fst < snd:
            return False
        elif not desc and snd < fst:
            return False
    return True


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n") if line]
    reports = [[int(n) for n in line.split()] for line in lines]
    print(sum(1 if is_safe(report) else 0 for report in reports))
    # do stuff with data
    s = 0
    print(
        sum(
            1 if (is_safe(report) or any(is_safe(d) for d in dampened(report))) else 0
            for report in reports
        )
    )
