"""Day 3 - Advent of Code"""
from string import ascii_letters
from typing import List

InputType = List[str]
PRIORITIES = dict(zip(ascii_letters, range(1, len(ascii_letters) + 1)))


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return fin.read().split("\n")


def solve_part_one(data: InputType) -> int:
    answer = 0

    for rucksack_items in data:
        N = len(rucksack_items)
        c1, c2 = rucksack_items[:N // 2], rucksack_items[N // 2:]

        common_items = set(c1).intersection(set(c2))
        assert len(common_items) == 1

        common_item = common_items.pop()

        answer += PRIORITIES[common_item]

    return answer


def solve_part_two(data: InputType, group_size: int = 3) -> int:
    answer = 0

    for idx in range(0, len(data), group_size):
        group = data[idx: idx + group_size]
        common_items = set.intersection(
            *(set(rucksack_items) for rucksack_items in group)
        )
        assert len(common_items) == 1

        common_item = common_items.pop()

        answer += PRIORITIES[common_item]

    return answer


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 157
            assert solution_two == 70

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
