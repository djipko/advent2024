#!/usr/bin/env python3
import re

mul_re_str = r"mul\((\d{1,3})\,(\d{1,3})\)"
mul_re = re.compile(mul_re_str)
inst_re = re.compile(rf"(do\(\))|(don't\(\))|{mul_re_str}")
if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    mem = "".join(lines)
    print(
        sum(int(match.group(1)) * int(match.group(2)) for match in mul_re.finditer(mem))
    )
    do_mul = True
    s = 0
    for match in inst_re.finditer(mem):
        if match.group(0) == "do()":
            do_mul = True
        elif match.group(0) == "don't()":
            do_mul = False
        elif do_mul and match:
            mul_match = mul_re.match(match.group(0))
            s += int(mul_match.group(1)) * int(mul_match.group(2))
    print(s)
