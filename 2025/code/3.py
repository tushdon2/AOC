from helpers import fetch, function_runner

banks = fetch(2025, 3).strip().split('\n')

def part1():
    # O(b^2) per bank, b = number of batteries in bank
    # SC: O(1)
    total = 0
    for bank in banks:
        sol = 0
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)): sol = max(sol, int(bank[i]+bank[j]))
        total += sol
    return total        


def part2(N=12):
    # O(N*b) per bank, b = number of batteries in bank
    # SC: O(N)
    total = 0
    for bank in banks:
        dp = [''] + [-1] * N
        sol = -1
        for d in range(len(bank) - 1, -1, -1):
            for n in range(N, 0, -1):
                take = int(bank[d] + dp[n - 1]) if dp[n - 1] != -1 else -1
                dp[n] = max(int(dp[n]), take)
                # not needed as no battery with 0 joltage
                # if bank[d] == '0' and dp[n] != -1 and len(str(dp[n])) < n: dp[n] = '0' + str(dp[n])
                if dp[n] != -1: dp[n] = str(dp[n])
            sol = max(sol, int(dp[N]))
        total += sol
    return total


def part1_optimised():
    # O(N*b) per bank, b = number of batteries in bank
    # SC: O(N)
    # N = 2
    return part2(2)

if __name__ == "__main__":
    function_runner(part1, part2, part1_optimised)

