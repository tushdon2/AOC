from helpers import fetch, function_runner

sets = []
# Merge overlapping ranges
for s, e in sorted(list(tuple(map(int, rng.split('-'))) 
                        for rng in fetch("2025", "2").split(','))):
    if len(sets) == 0 or sets[-1][1] < s - 1:
        sets.append([s, e])
    else:
        sets[-1][1] = max(sets[-1][1], e)


def part1():
    total = 0
    for s, e in sets:
        for i in range(s, e + 1):
            num = str(i)
            l = len(num)
            if l % 2 == 0 and num[:l//2] == num[l//2:]: total += i
    return total


def part2():
    def check_repeat(num:str) -> bool:
        l = len(num)
        for size in range(1, l // 2 + 1):
            if l % size == 0:
                part = num[:size]
                if part * (l // size) == num:
                    return True            
        return False
    
    total = 0
    for s, e in sets:
        for i in range(s, e + 1):
            if check_repeat(str(i)): total += i
    return total
    

if __name__ == "__main__":
    function_runner(part1, part2)

