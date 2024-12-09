#!/usr/bin/env python3
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
import heapq
from sortedcontainers import SortedList


@dataclass(order=True)
class Span:
    len: int
    pos: int
    f_id: int | None
    next: Span | None = field(compare=False, default=None)
    prev: Span | None = field(compare=False, default=None)


@dataclass
class Disk:
    empty_spans: SortedList[Span]
    f_by_id: dict[int, Span]
    start: Span | None
    end: Span | Disk | None = None

    def append(self, s: Span):
        if not self.start:
            assert not self.start
            self.start = s
            self.end = s
        else:
            assert s.next is None
            self.end.next = s
            s.prev = self.end
            self.end = s
        if s.f_id is None:
            self.empty_spans.add(s)
        else:
            self.f_by_id[s.f_id] = s

    def find_empty_for(self, s: Span) -> Span | None:
        e = None
        idx = self.empty_spans.bisect_left(Span(s.len, -1, None))
        for maybe_e in self.empty_spans[idx:]:
            if maybe_e.len >= s.len and maybe_e.pos < s.pos:
                e = maybe_e
                self.empty_spans.remove(e)
                break
        return e

    def fit_into(self, empty: Span, s: Span):
        s_next = s.next
        s_prev = s.prev

        if empty.prev:
            empty.prev.next = s
        if empty.next:
            empty.next.prev = s
        s.prev = empty.prev
        s.next = empty.next

        if s_prev:
            s_prev.next = empty
        if s_next:
            s_next.prev = empty
        empty.prev = s_prev
        empty.next = s_next
        empty.pos, s.pos = s.pos, empty.pos

        if empty.len > s.len:
            new_empty = Span(empty.len - s.len, s.pos + s.len, None)
            new_empty.prev = s
            new_empty.next = s.next
            s.next = new_empty
            new_empty.next.prev = new_empty
            self.empty_spans.add(new_empty)
        # Reduce the size of the old empty that is now moved
        empty.len = s.len

    def validate_pos(self):
        cur = self.start
        while cur.next:
            assert cur.next.pos == cur.pos + cur.len
            cur = cur.next

    def move_span(self, s: Span):
        e = self.find_empty_for(s)
        if e:
            self.fit_into(e, s)
            self.validate_pos()

    def defrag(self):
        for f_id, span in reversed(self.f_by_id.items()):
            self.move_span(span)
            # print(self.print_layout())

    def print_layout(self):
        cur = self.start
        s = []
        while cur:
            s.extend([str(cur.f_id) if cur.f_id is not None else "."] * cur.len)
            cur = cur.next
        return "".join(s)

    def checksum(self):
        cur = self.start
        cs = 0
        while cur:
            if cur.f_id is not None:
                for idx in range(cur.len):
                    cs += (cur.pos + idx) * cur.f_id
            cur = cur.next
        return cs


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


def parse_diskmap2(diskmap):
    empty = False
    f_id = 0
    disk = Disk(SortedList(), {}, None)
    pos = 0
    for s in diskmap:
        l = int(s)
        if empty:
            s = Span(l, pos, None)
        else:
            s = Span(l, pos, f_id)
            f_id += 1
        disk.append(s)
        empty = not empty
        pos += l
    return disk


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
    disk = parse_diskmap2(diskmap)
    print(disk.print_layout())
    disk.defrag()
    print(disk.print_layout())
    print(disk.checksum())
