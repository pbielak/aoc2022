"""Day 4 - Advent of Code"""
from typing import List, NamedTuple, Tuple


class Range(NamedTuple):
    min: int
    max: int

    @classmethod
    def from_string(cls, raw: str) -> "Range":
        min, max = raw.split("-")

        return cls(min=int(min), max=int(max))

    def contains(self, other: "Range") -> bool:
        return (
            self.min <= other.min <= self.max
            and self.min <= other.max <= self.max
        )

    def overlaps(self, other: "Range") -> bool:
        return (
            (self.min <= other.min <= self.max)
            or (self.min <= other.max <= self.max)
        )


InputType = List[Tuple[Range, Range]]


def read_data(path: str) -> InputType:
    data = []
    with open(path, "r") as fin:
        for line in fin:
            r1, r2 = line.split(",")
            data.append((Range.from_string(r1), Range.from_string(r2)))

    return data


def solve_part_one(data: InputType) -> int:
    return sum(1 for r1, r2 in data if r1.contains(r2) or r2.contains(r1))


def solve_part_two(data: InputType) -> int:
    return sum(1 for r1, r2 in data if r1.overlaps(r2) or r2.overlaps(r1))


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 2
            assert solution_two == 4

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
