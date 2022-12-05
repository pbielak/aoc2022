"""Day 5 - Advent of Code"""
from copy import deepcopy
from typing import List, NamedTuple, Tuple

StackType = List[str]


class Move(NamedTuple):
    N: int
    src: int
    dst: int

    @classmethod
    def from_string(cls, raw: str) -> "Move":
        n, src, dst = (
            raw
            .replace("move ", "")
            .replace("from ", "")
            .replace("to ", "")
            .split(" ")
        )

        return cls(N=int(n), src=int(src), dst=int(dst))


InputType = Tuple[StackType, List[Move]]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        _, moves_raw = fin.read().split("\n\n")

        # Parsing those stacks would be a waste of time - let's hardcode them
        if path == "data/example.txt":
            stacks = ["NZ", "DCM", "P"]
        elif path == "data/input.txt":
            stacks = [
                "VJBD",
                "FDRWBVP",
                "QWCDLFGR",
                "BDNLMPJW",
                "QSCPBNH",
                "GNSBDR",
                "HSFQMPBZ",
                "FLW",
                "RMFVS",
            ]
        else:
            raise RuntimeError("Should not happen!")

        moves = [Move.from_string(line) for line in moves_raw.split("\n")]

        return stacks, moves


def solve_part_one(data: InputType) -> str:
    stacks, moves = deepcopy(data)

    for move in moves:
        for _ in range(move.N):
            c = stacks[move.src - 1][0]
            stacks[move.src - 1] = stacks[move.src - 1][1:]
            stacks[move.dst - 1] = c + stacks[move.dst - 1]

    answer = "".join([stack[0] for stack in stacks])
    return answer


def solve_part_two(data: InputType) -> str:
    stacks, moves = deepcopy(data)

    for move in moves:
        c = stacks[move.src - 1][:move.N]
        stacks[move.src - 1] = stacks[move.src - 1][move.N:]
        stacks[move.dst - 1] = c + stacks[move.dst - 1]

    answer = "".join([stack[0] for stack in stacks])
    return answer


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == "CMZ"
            assert solution_two == "MCD"

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
