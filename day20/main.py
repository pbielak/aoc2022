"""Day 20 - Advent of Code"""
from typing import List, Tuple

InputType = List[Tuple[int, int]]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return [
            (idx, int(number.strip()))
            for idx, number in enumerate(fin.readlines())
        ]


def mix(input_data: InputType, to_mix: InputType) -> InputType:
    mixed = to_mix.copy()

    for original_idx, original_value in input_data:
        idx = mixed.index((original_idx, original_value))

        del mixed[idx]

        new_idx = (idx + original_value) % len(mixed)

        if new_idx < 0:
            new_idx += len(mixed)

        mixed.insert(new_idx, (original_idx, original_value))

    return mixed


def solve_part_one(data: InputType) -> int:
    out = mix(input_data=data, to_mix=data)
    out = [number for _, number in out]

    zero_idx = out.index(0)
    answer = (
        out[(zero_idx + 1000) % len(out)]
        + out[(zero_idx + 2000) % len(out)]
        + out[(zero_idx + 3000) % len(out)]
    )
    return answer


def solve_part_two(data: InputType) -> int:
    decryption_key = 811_589_153
    input_data = [(idx, number * decryption_key) for idx, number in data]

    out = input_data.copy()
    for _ in range(10):
        out = mix(input_data=input_data, to_mix=out)

    out = [number for _, number in out]
    zero_idx = out.index(0)
    answer = (
        out[(zero_idx + 1000) % len(out)]
        + out[(zero_idx + 2000) % len(out)]
        + out[(zero_idx + 3000) % len(out)]
    )
    return answer


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 3
            assert solution_two == 1_623_178_306

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
