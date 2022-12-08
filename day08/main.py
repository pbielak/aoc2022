"""Day 8 - Advent of Code"""
from typing import Tuple

InputType = Tuple[Tuple[int]]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return tuple(
            tuple(int(height) for height in line)
            for line in fin.read().split("\n")
        )


def is_visible(pos_i: int, pos_j: int, data: InputType) -> bool:
    width, height = len(data[0]), len(data)

    tree_height = data[pos_i][pos_j]

    # Top
    if all(data[i][pos_j] < tree_height for i in range(pos_i)):
        return True

    # Bottom
    if all(data[i][pos_j] < tree_height for i in range(pos_i + 1, height)):
        return True

    # Left
    if all(data[pos_i][j] < tree_height for j in range(pos_j)):
        return True

    # Right
    if all(data[pos_i][j] < tree_height for j in range(pos_j + 1, width)):
        return True

    return False


def solve_part_one(data: InputType) -> int:
    width, height = len(data[0]), len(data)

    num_visible = 0

    # Add border
    num_visible += 2 * width + 2 * (height - 2)

    # Check interior
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if is_visible(i, j, data):
                num_visible += 1

    return num_visible


def compute_scenic_score(pos_i: int, pos_j: int, data: InputType) -> int:
    width, height = len(data[0]), len(data)

    tree_height = data[pos_i][pos_j]

    # Top
    dist_top = 0
    for i in reversed(range(pos_i)):
        dist_top += 1

        if data[i][pos_j] >= tree_height:
            break

    # Bottom
    dist_bottom = 0
    for i in range(pos_i + 1, height):
        dist_bottom += 1

        if data[i][pos_j] >= tree_height:
            break

    # Left
    dist_left = 0
    for j in reversed(range(pos_j)):
        dist_left += 1

        if data[pos_i][j] >= tree_height:
            break

    # Right
    dist_right = 0
    for j in range(pos_j + 1, width):
        dist_right += 1

        if data[pos_i][j] >= tree_height:
            break

    return dist_top * dist_bottom * dist_left * dist_right


def solve_part_two(data: InputType) -> int:
    width, height = len(data[0]), len(data)

    max_scenic_score = 0

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            scenic_ij = compute_scenic_score(i, j, data)
            max_scenic_score = max(max_scenic_score, scenic_ij)

    return max_scenic_score


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 21
            assert solution_two == 8

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
