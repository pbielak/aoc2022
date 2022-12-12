"""Day 12 - Advent of Code"""
from __future__ import annotations

import heapq
import sys
from typing import Dict, List, Tuple


Position = Tuple[int, int]
Adj = Dict[Position, List[Position]]
Weights = Dict[Position, int]
InputType = List[List[str]]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return [
            [height_character for height_character in line.strip()]
            for line in fin.readlines()
        ]


def to_adj(data: InputType) -> Tuple[Adj, Weights]:
    adj = {}
    weights = {}
    for i in range(len(data)):
        for j in range(len(data[0])):
            adj[(i, j)] = neighbors((i, j), data)
            weights[(i, j)] = 1

    return adj, weights


def neighbors(pos: Position, data: InputType) -> List[Position]:
    neighborhood = []

    for i, j in (
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
    ):
        if not (0 <= i < len(data)):
            continue

        if not (0 <= j < len(data[0])):
            continue

        if data[i][j] == "E":
            target_height = ord("z")
        else:
            target_height = ord(data[i][j])

        if data[pos[0]][pos[1]] == "S":
            source_height = ord("a")
        else:
            source_height = ord(data[pos[0]][pos[1]])

        if target_height - source_height <= 1 and data[i][j] != "S":
            neighborhood.append((i, j))

    return neighborhood


class NodePriorityQueue:

    def __init__(self):
        self._nodes_pq = []

    def add(self, node: Position, weight: int):
        heapq.heappush(self._nodes_pq, (weight, node))

    def pop(self) -> Tuple[int, Position]:
        return heapq.heappop(self._nodes_pq)

    def __len__(self) -> int:
        return len(self._nodes_pq)


def dijkstra(
    adj: Adj,
    weights: Weights,
    start_pos: Position,
    target_pos: Position,
) -> Dict[Position, int]:
    """Based on `https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/`"""
    Q = NodePriorityQueue()

    dist = {}

    for v in adj.keys():
        dist[v] = sys.maxsize

    dist[start_pos] = 0
    Q.add(node=start_pos, weight=0)

    while len(Q) > 0:
        dist_u, u = Q.pop()

        if dist_u > dist[u]:
            continue

        if u == target_pos:
            break

        for v in adj[u]:
            alt = dist_u + weights[v]
            if alt < dist[v]:
                dist[v] = alt
                Q.add(node=v, weight=alt)

    return dist


def find_start_and_end_positions(data: InputType) -> Tuple[Position, Position]:
    s_pos = None
    e_pos = None

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "S":
                s_pos = (i, j)
            if data[i][j] == "E":
                e_pos = (i, j)

    assert s_pos is not None and e_pos is not None
    return s_pos, e_pos


def solve_part_one(data: InputType) -> int:
    s_pos, e_pos = find_start_and_end_positions(data)
    adj, weights = to_adj(data)

    dist = dijkstra(
        adj=adj,
        weights=weights,
        start_pos=s_pos,
        target_pos=e_pos,
    )

    return dist[e_pos]


def solve_part_two(data: InputType) -> int:
    s_pos, e_pos = find_start_and_end_positions(data)
    data[s_pos[0]][s_pos[1]] = "a"  # Remove the start position

    a_positions = [
        (i, j)
        for i in range(len(data))
        for j in range(len(data[0]))
        if data[i][j] == "a"
    ]

    min_dist = 9999

    for i, j in a_positions:
        data[i][j] = "S"

        adj, weights = to_adj(data)
        dist = dijkstra(
            adj=adj,
            weights=weights,
            start_pos=(i, j),
            target_pos=e_pos,
        )

        min_dist = min(min_dist, dist[e_pos])

        data[i][j] = "a"

    return min_dist


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 31
            assert solution_two == 29

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
