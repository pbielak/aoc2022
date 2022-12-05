"""Day 1 - Advent of Code"""
from typing import List

InputType = List[List[int]]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return [
            [int(cal) for cal in elf_calories.split("\n")]
            for elf_calories in fin.read().split("\n\n")
        ]


def solve_part_one(data: InputType) -> int:
    return max(map(sum, data))


def solve_part_two(data: InputType, top_k: int = 3) -> int:
    return sum(sorted(map(sum, data), reverse=True)[:top_k])


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
