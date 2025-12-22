from helpers import fetch, function_runner
import math

# NON-RIGOROUS SOLUTION
# Solved it after seeing this discussion on Reddit:
# https://www.reddit.com/r/adventofcode/comments/1pkje0o/2025_day_12_solutions/
# Apparently, the test case is not as hard as portrayed in the example test case
# Notice that all gifts can fit within grid size 3x3, just find the area of under tree and 
# it should be more than # of gifts * 9, i.e. try arranging gifts as square boxes
# Don't try to optimise the arrangement

grids = [[tuple(map(int, line.split(':')[0].split('x'))), 
          tuple(map(int, line.split(':')[1].strip().split()))] 
         for line in fetch(2025, 12).splitlines() if 'x' in line]

def part1():
    return sum(math.prod(i) >= 9 * sum(j) for i, j in grids)


if __name__ == "__main__":
    function_runner(part1)
