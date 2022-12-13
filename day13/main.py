"""Day 13 - Advent of Code"""
from copy import deepcopy
from functools import cmp_to_key
from typing import List, Tuple

Packet = list
InputType = List[Tuple[Packet, Packet]]


def read_data(path: str) -> InputType:
    packets = []
    with open(path, "r") as fin:
        for packet_pair in fin.read().split("\n\n"):
            p1, p2 = packet_pair.split("\n")
            packets.append((eval(p1), eval(p2)))
    return packets


def compare(left: Packet, right: Packet) -> int:
    for l, r in zip(left, right):
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return 1
            if l > r:
                return -1
        elif isinstance(l, list) and isinstance(r, list):
            res = compare(l, r)
            if res in (1, -1):
                return res
        else:
            if isinstance(l, int):
                l = [l]

            if isinstance(r, int):
                r = [r]

            res = compare(l, r)

            if res in (1, -1):
                return res

    if len(left) < len(right):
        return 1

    if len(left) > len(right):
        return -1

    return 0


def solve_part_one(data: InputType) -> int:
    answer = 0

    for idx, (p1, p2) in enumerate(data, start=1):
        res = compare(p1, p2)
        if res == 1:  # Is ordered
            answer += idx

    return answer


def solve_part_two(data: InputType) -> int:
    divider_packets = [[[2]], [[6]]]
    packet_pairs = deepcopy(data)
    packets = [packet for pair in packet_pairs for packet in pair]
    packets.extend(divider_packets)
    sorted_packets = sorted(packets, key=cmp_to_key(compare), reverse=True)

    answer = (
        (sorted_packets.index(divider_packets[0]) + 1)
        * (sorted_packets.index(divider_packets[1]) + 1)
    )

    return answer


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 13
            assert solution_two == 140

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
