from helpers import fetch
from time import time

data = list(map(int, fetch("2025", "1").replace('R', '').replace('L', '-').split('\n')))

def part1():
    cnt, pos = 0, 50
    for mov in data:
        pos = (pos + mov) % 100
        if pos == 0: cnt += 1
    return cnt

def part2():
    cnt, pos = 0, 50
    for mov in data:
        q, new_pos = divmod(pos + mov, 100)
        q = abs(q)
        if mov < 0: q += (new_pos == 0) - (pos == 0)
        # if mov == 0 and pos == 0: q = 1 # not needed since no zero moves in input
        cnt += q
        pos = new_pos
    return cnt

if __name__ == "__main__":
    SOLS = [part1, part2]
    for fn in SOLS:
        st = time()
        print(fn())
        print(f"Ran {fn.__name__} in {time() - st:.4f} seconds")

