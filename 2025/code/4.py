from helpers import fetch, function_runner

grid = [list(row) for row in fetch(2025, 4).strip().split('\n')]

def part1():
    cnt = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '@':
                left = grid[i][j-1] == '@' if j > 0 else False
                right = grid[i][j+1] == '@' if j < len(grid[0]) - 1 else False
                up = grid[i-1][j] == '@' if i > 0 else False
                down = grid[i+1][j] == '@' if i < len(grid) - 1 else False
                left_up = grid[i-1][j-1] == '@' if i > 0 and j > 0 else False
                left_down = grid[i+1][j-1] == '@' if i < len(grid) - 1 and j > 0 else False
                right_up = grid[i-1][j+1] == '@' if i > 0 and j < len(grid[0]) - 1 else False
                right_down = grid[i+1][j+1] == '@' if i < len(grid) - 1 and j < len(grid[0]) - 1 else False
                cnt += (sum([left, right, up, down, left_up, left_down, right_up, right_down]) < 4)
    return cnt


def part2():
    total = 0
    while True:
        cnt = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '@':
                    left = grid[i][j-1] == '@' if j > 0 else False
                    right = grid[i][j+1] == '@' if j < len(grid[0]) - 1 else False
                    up = grid[i-1][j] == '@' if i > 0 else False
                    down = grid[i+1][j] == '@' if i < len(grid) - 1 else False
                    left_up = grid[i-1][j-1] == '@' if i > 0 and j > 0 else False
                    left_down = grid[i+1][j-1] == '@' if i < len(grid) - 1 and j > 0 else False
                    right_up = grid[i-1][j+1] == '@' if i > 0 and j < len(grid[0]) - 1 else False
                    right_down = grid[i+1][j+1] == '@' if i < len(grid) - 1 and j < len(grid[0]) - 1 else False
                    
                    if sum([left, right, up, down, left_up, left_down, right_up, right_down]) < 4:
                        cnt += 1
                        grid[i][j] = '.'
        if cnt == 0: return total
        total += cnt
    

if __name__ == "__main__":
    function_runner(part1, part2)

