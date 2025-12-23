from helpers import fetch, function_runner
from collections import defaultdict
from itertools import combinations


light_status, buttons_list, joltages = [], [], []
for line in fetch(2025, 10).splitlines():
    buttons = []
    for item in line.split():
        if item[0] == "[": light_status.append(tuple(i == "#" for i in item[1:-1]))
        elif item[0] == "(": buttons.append(tuple(map(int, item[1:-1].split(','))))
        elif item[0] == "{": joltages.append(tuple(map(int, item[1:-1].split(','))))
    buttons_list.append(buttons)


def _recurse(idx, curr_stat, final, buttons):
    if curr_stat == final: return 0
    if idx == len(buttons): return float('inf')
    
    no_press = _recurse(idx + 1, curr_stat, final, buttons)
    curr_stat = tuple((not s) if i in buttons[idx] else s for i, s in enumerate(curr_stat))
    press = 1 + _recurse(idx + 1, curr_stat, final, buttons)

    return min(press, no_press)

def part1():    
    return sum(_recurse(0, tuple(False for _ in status), status, buttons)
               for status, buttons in zip(light_status, buttons_list))


def _recurse_joltage(idx, memo, cur_jolt, req_jolt, buttons):
    # if joltage array is [J1, J2.... Jn], and there are B buttons
    # max TC and SC: O(B*J1*J2.....*Jn): TOO MUCH
    if (cur_jolt == req_jolt): return 0
    if idx >= len(buttons): return float('inf')
    
    key = (idx, *cur_jolt)
    if key in memo: return memo[key]
    
    no_press = _recurse_joltage(idx + 1, memo, cur_jolt, req_jolt, buttons)
    new_jolt = tuple(j + (i in buttons[idx]) for i, j in enumerate(cur_jolt))
    if all(i >= j for i, j in zip(req_jolt, new_jolt)): 
        press = 1 + _recurse_joltage(idx, memo, new_jolt, req_jolt, buttons)
    else: press = float('inf')
    
    memo[key] = min(no_press, press)
    return memo[key]

def part2():
    # takes a hell lot of time
    return sum(_recurse_joltage(0, {}, tuple(0 for _ in joltage), joltage, buttons) 
               for joltage, buttons in zip(joltages, buttons_list))


def _press_once_possibilities(buttons, n_counters):
    buttons_vectorised = [[1 if cnt in b else 0 for cnt in range(n_counters)] for b in buttons]
    # what all sums can we get by pressing any button at max once
    # 1st key: boolean status after pressing all selected keys
    # 2nd key: sum status after pressing all keys
    # value = number of keys pressed
    possibilities = defaultdict(lambda: defaultdict(int))
    # no button press needed to move counter states to all 0
    possibilities[(0, ) * n_counters][(0, ) * n_counters] = 0

    for n_presses in range(len(buttons) + 1):
        for button_idxs in combinations(range(len(buttons)), n_presses):
            key2 = tuple(map(sum, zip((0, ) * n_counters, *(buttons_vectorised[i] for i in button_idxs))))
            key1 = tuple(j % 2 for j in key2)
            possibilities[key1][key2] = n_presses if not possibilities[key1][key2] else min(possibilities[key1][key2], n_presses)

    return possibilities

def _divide_n_conquer(joltage, blank, possibilities, memo={}):
    # got this fantistic solution here:
    # https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
    # but it has some pitfalls too, where this algo fails
    if (joltage == blank): return 0
    if joltage in memo: return memo[joltage]
    # solve part one for non even part of the joltage array: 
    # gives the number of button presses to achieve the odd part from precalculated possibilities 
    memo[joltage] = float('inf')
    odd_part = tuple(j % 2 for j in joltage)
    for sums, presses in possibilities[odd_part].items(): 
        # accordingly get new half joltages
        new_jolt = tuple((j - i) // 2 for i, j in zip(sums, joltage))
        memo[joltage] = min(memo[joltage], presses + 2 * _divide_n_conquer(new_jolt, blank, possibilities, memo))
    return memo[joltage]

def part2_efficient():
    return sum(_divide_n_conquer(joltage, tuple(0 for _ in joltage), 
                                 _press_once_possibilities(buttons, len(joltage)), memo={}) 
                                 for joltage, buttons in zip(joltages, buttons_list))

# PART 2 by GAUSSIAN ELIMINATION and FREE VARIABLES:
# https://www.reddit.com/r/adventofcode/comments/1plzhps/2025_day_10_part_2_pivot_your_way_to_victory/
# https://math.libretexts.org/Bookshelves/Linear_Algebra/Map%3A_Linear_Algebra_(Waldron_Cherney_and_Denton)/02%3A_Systems_of_Linear_Equations
# Get Augmented matrix for Ax = b: A_aug = [A | b]
# each col of A = vectorised buttons, x = count of button presses, b = joltage goals
# get Row-Reduced-Echelon-Form: then get free variables from here
# Get general solution of these set of equations: X = X_particular + sum(free_var_i * X_homogenous_i)
# Minimise the sum of variables: on the constraint that each of them is positive and integral
# Can use scipy.linprog to achieve this

if __name__ == "__main__": 
    function_runner(part1, part2_efficient,
                    # part2 # too much time 
                    )