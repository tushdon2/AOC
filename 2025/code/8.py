from collections import defaultdict
from helpers import fetch, function_runner
from itertools import combinations
import math


points = list(tuple(map(int, row.split(','))) for row in fetch(2025, 8).splitlines())
sorted_point_pairs = []
def order_points_by_dist():
    # takes most of the code run time: its time should be added to part 1 and 2 run times
    # O(N^2 * log(N))
    l2_norm_sq = lambda p1, p2: sum((f-s)**2 for f, s in zip(p1, p2)) 
    for p1, p2 in combinations(range(len(points)), 2): # O(N^2)
        sorted_point_pairs.append((l2_norm_sq(points[p1], points[p2]), p1, p2))
    sorted_point_pairs.sort() # makes it O(N^2 * log(N^2)) = O(N^2 * log(N))


def part1():
    N = 1000
    ad_list = defaultdict(set)
    for _, p1, p2 in sorted_point_pairs[:N]:
        ad_list[p1].add(p2)
        ad_list[p2].add(p1)

    # O(V+E)
    visited, circuits = set(), []
    def _dfs(idx:int):
        visited.add(idx)
        for i in ad_list[idx]: 
            if i not in visited: _dfs(i)

    for i in ad_list.keys():
        int_cnt = len(visited)
        if i not in visited: 
            _dfs(i)
            circuits.append(len(visited) - int_cnt)
    return math.prod(sorted(circuits, reverse=True)[:3])


def part2():
    node_id = {i:i for i in range(len(points))}
    ad_list = {i:{i} for i in range(len(points))}
    for _, p1, p2 in sorted_point_pairs:
        if node_id[p1] == node_id[p2]: continue
        if len(ad_list[node_id[p1]]) < len(ad_list[node_id[p2]]):
            p1, p2 = p2, p1
        nodes = ad_list[node_id[p2]]
        del ad_list[node_id[p2]]
        for node in nodes: node_id[node] = node_id[p1]
        ad_list[node_id[p1]].update(nodes)
        if len(ad_list.keys()) == 1: 
            return points[p1][0] * points[p2][0]
        

def part1_another_way():
    # similar to part 2
    node_id = {i:i for i in range(len(points))}
    ad_list = {i:{i} for i in range(len(points))}
    for _, p1, p2 in sorted_point_pairs[:1000]:
        if node_id[p1] == node_id[p2]: continue
        if len(ad_list[node_id[p1]]) < len(ad_list[node_id[p2]]):
            p1, p2 = p2, p1
        nodes = ad_list[node_id[p2]]
        del ad_list[node_id[p2]]
        for node in nodes: node_id[node] = node_id[p1]
        ad_list[node_id[p1]].update(nodes)

    return math.prod(len(p) for p in sorted(ad_list.values(), 
                                            key=lambda x: len(x), reverse=True)[:3])


if __name__ == "__main__":
    function_runner(order_points_by_dist, part1, part2, part1_another_way)
