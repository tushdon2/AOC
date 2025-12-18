from helpers import *
import math
import re

lines = fetch(2025, 6).split("\n")

def part1():
    nums_and_operations = []
    for line in lines[:-1]: nums_and_operations.append(list(map(int, re.findall(r"\d+", line))))
    nums_and_operations.append(re.findall(r"[+*]+", lines[-1]))

    total = 0
    for problem in zip(*nums_and_operations):
        if problem[-1] == "+": total += sum(problem[:-1])
        else: total += math.prod(problem[:-1])

    return total


def part2():
    for i in range(len(lines)):
        lines[i] = list(lines[i]) + [" "]

    total, nums, opr = 0, [], ""
    for inp in zip(*lines):
        opr = inp[-1] if inp[-1] != " " else opr
        num = ''.join(inp[:-1]).strip()
        if num: nums.append(int(num))
        elif opr == "+": 
            total += sum(nums)
            nums = []
        elif opr == "*":
            total += math.prod(nums)
            nums = []

    return total
        

if __name__ == "__main__":
    function_runner(part1, part2)