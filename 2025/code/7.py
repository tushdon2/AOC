from helpers import fetch, function_runner

"""
-   The problem doesn't discuss what if two splitters are adjacent in a row, e.g. ".^..^^...."
    Will the new beam start from the nearest adjacent empty space? 
    .|..|.....      ->      .|..|.....           
    .^..^^....              |^||^^|...
    Or will it just stop for the adjacent splitter, assuming splitters work only if the beam comes to it from previous row?  
    .|..|.....      ->      .|..|.....           
    .^..^^....              |^||^^....

-   It also evades the case when a split beam hits Tachyon Manifold boundary, 
    e.g. if splitter placement is like: "^......" and a beam hits it, the split beam can't go leftward

Thankfully, such cases don't exist in the example or the test case.
"""

lines = [[False if ch == '.' else True for ch in line] for line in fetch(2025, 7).strip().split("\n")]

def part1():
    cnt, h, w = 0, len(lines), len(lines[0])
    mask = lines[0]
    for i in range(1, h):
        bin_and = [a and b for a, b in zip(mask, lines[i])]
        cnt += sum(bin_and)
        newmask = [False] * w
        for j in range(w):
            if bin_and[j]:
                if j > 0: newmask[j - 1] = True
                if j < w - 1: newmask[j + 1] = True
            elif mask[j]: newmask[j] = True
        mask = newmask
    return cnt


def part2():
    h, w = len(lines), len(lines[0])
    timelines = lines[0]
    for i in range(1, h):
        for j in range(w):
            if lines[i][j] and timelines[j]:
                if j > 0: timelines[j-1] += timelines[j]
                if j < w - 1: timelines[j+1] += timelines[j]
                timelines[j] = 0
    return sum(timelines)        


if __name__ == "__main__":
    function_runner(part1, part2)