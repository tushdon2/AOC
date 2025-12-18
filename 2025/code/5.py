from helpers import fetch, function_runner

sets, ids = [], set()
for line in fetch(2025, 5).splitlines():
    if '-' in line: sets.append(tuple(map(int, line.split('-'))))
    elif line.strip(): ids.add(int(line))

# Preprocessing: Merge overlapping ranges
# This code will take some small amount of time too and 
# should ideally be added to time taken of part 1 and 2 
merged_sets = []
def merge_ranges():
    for s, e in sorted(sets):
        if len(merged_sets) == 0 or merged_sets[-1][1] < s - 1: merged_sets.append([s, e])
        else: merged_sets[-1][1] = max(merged_sets[-1][1], e)


def part1():
    total = 0
    for i in ids:
        for s, e in merged_sets:
            if s <= i <= e:
                total += 1
                break
    return total


def part2():
    total = 0
    for s, e in merged_sets: total += e - s + 1
    return total
        

if __name__ == "__main__":
    function_runner(merge_ranges, part1, part2)

