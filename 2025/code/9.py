from collections import deque
from helpers import fetch, function_runner
from itertools import combinations
from shapely import Polygon
import random


points = list(tuple(map(int, row.split(','))) for row in fetch(2025, 9).splitlines())
area = lambda p1, p2: (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
rect = lambda p1, p2: [p1, (p1[0], p2[1]), p2, (p2[0], p1[1])]


def part1():
    return max(area(p1, p2) for p1, p2 in combinations(points, 2))


def part2_cheap_way():
    # found this here: cheating a bit
    # https://github.com/salt-die/Advent-of-Code/blob/main/2025/day_09.py
    polygon = Polygon(points)
    return max(area(a, b) for a, b in combinations(points, 2) 
               if polygon.covers(Polygon(rect(a, b))))


def _is_point_inside_polygon(point:tuple[int], polygon=points) -> bool:
    # Ray Tracing Algo: 
    # For point under consideration, check how many times a ray originating from that point
    # towards +ve x direction hits any edge of polygon. 
    # If odd # of times: point is inside the polygon, otherwise not.
    # Assuming points in polygon list are in either clockwise or anti-clockwise direction
    x, y = point
    is_inside, n = False, len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        # here we have only horizontal and vertical edges 
        # so the conditions of intersection have simplified
        if ((y1 > y) != (y2 > y) and # the two points should be in opposite side of ray
            x < x1): # the point should be behind the intersection point of ray with the edge
            is_inside = not is_inside

    return is_inside

def _get_all_boundary_points(polygon=points) -> set[tuple[int]]:
    all_points = set(polygon)
    n = len(polygon)

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if y1 == y2: all_points.update((x, y1) for x in range(min(x1, x2) + 1, max(x1, x2)))
        if x1 == x2: all_points.update((x1, y) for y in range(min(y1, y2) + 1, max(y1, y2)))

    return all_points

def part2():
    # ray tracing based judgement for all points on a rectangle formed by two points on polygon
    # ran in ~2 hrs on my hardware for given test case
    # can be improved further by vectorising it using numpy
    inside_points = set()
    polygon_boundary = _get_all_boundary_points()
    ans = 0

    for p1, p2 in combinations(points, 2):
        is_covered = True
        for p in _get_all_boundary_points(rect(p1, p2)): 
            if p in inside_points or p in polygon_boundary: continue
            if not _is_point_inside_polygon(p): 
                is_covered = False
                break
            inside_points.add(p)
        if is_covered: ans = max(ans, area(p1, p2))

    return ans


def _flood_fill_bfs(polygon=points) -> set[tuple[int]]:
    max_x, max_y = max(x for x, _ in polygon), max(y for _, y in polygon)
    min_x, min_y = min(x for x, _ in polygon), min(y for _, y in polygon)

    seed = ((min_x + max_x) // 2, (min_y + max_y) // 2)
    while (not _is_point_inside_polygon(seed)):
        seed = (random.randint(min_x, max_x), random.randint(min_y, max_y))

    q = deque([seed])
    visited = _get_all_boundary_points()
    while q: 
        p = q.popleft()
        visited.add(p)
        for dx, dy in [(1,1), (1,-1), (-1,-1), (-1,1)]:
            pn = p[0] + dx, p[1] + dy
            if pn not in visited: q.append(pn)

    return visited

def part2_flood_fill():
    # my device went OOM
    all_inside_points = _flood_fill_bfs()
    sol = 0

    for p1, p2 in combinations(points, 2):
        is_covered = True
        for p in _get_all_boundary_points(rect(p1, p2)): 
            if p not in all_inside_points: 
                is_covered = False
                break
        if is_covered: sol = max(sol, area(p1, p2))

    return sol


if __name__ == "__main__":
    function_runner(part1, 
                    # part2, # 2 hrs
                    # part2_flood_fill, # very inefficient
                    part2_cheap_way)
