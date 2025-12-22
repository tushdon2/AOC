from helpers import fetch, function_runner


ad_list = {line.strip().split(':')[0]: line.strip().split(':')[1].strip().split() for line in fetch(2025, 11).splitlines()}


def _num_paths_dfs(node, memo, adj_list=ad_list):
    # add destination node count as 1 while initialising
    # assuming there are no cyclical paths between any nodes
    if node in memo: return memo[node]

    memo[node] = 0
    for child in adj_list[node]:
        memo[node] += _num_paths_dfs(child, memo, adj_list)

    return memo[node]

def part1(): 
    return _num_paths_dfs('you', {'out': 1})


def part2():
    # must not go to 'out' before going to the other intermediary node
    fft2dac = _num_paths_dfs('fft', {'dac': 1, 'out': 0})
    dac2fft = _num_paths_dfs('dac', {'fft': 1, 'out': 0})

    # assuming there are no cyclical paths between any nodes
    # then either there is a path between fft to dac, or vice-versa
    ans = 0
    if fft2dac:
        svr2fft = _num_paths_dfs('svr', {'fft': 1, 'out': 0})
        dac2out = _num_paths_dfs('dac', {'out': 1})
        ans += svr2fft * fft2dac * dac2out
    if dac2fft:
        svr2dac = _num_paths_dfs('svr', {'dac': 1, 'out': 0})
        fft2out = _num_paths_dfs('fft', {'out': 1})
        ans += svr2dac * dac2fft * fft2out
    return ans


def _num_paths_fft_dac(node, fft_vis, dac_vis, memo, adj=ad_list):
    if node == 'fft': fft_vis = True
    elif node == 'dac': dac_vis = True

    key = (node, fft_vis, dac_vis)
    if key in memo: return memo[key]

    memo[key] = 0
    for child in adj[node]:
        memo[key] += _num_paths_fft_dac(child, fft_vis, dac_vis, memo)
    
    return memo[key] 
    
def part2_another_way():
    return _num_paths_fft_dac('svr', False, False, 
                              {('out', i, j): int(i and j )
                               for i in [False, True] for j in [False, True]})


if __name__ == "__main__":
    function_runner(part1, part2, part2_another_way)