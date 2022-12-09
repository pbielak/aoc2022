"""Day 9 - Advent of Code"""
from typing import Dict, List, NamedTuple, Tuple

DirectionVector = Tuple[int, int]
InputType = List[Tuple[DirectionVector, int]]


class Position(NamedTuple):
    x: int
    y: int


def read_data(path: str) -> InputType:
    direction_vectors = {
        "U": (0, -1),
        "D": (0, 1),
        "L": (-1, 0),
        "R": (1, 0),
    }

    instructions = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            direction, steps = line.strip().split(" ")
            instructions.append((direction_vectors[direction], int(steps)))
    return instructions


def is_adjacent(x1: int, y1: int, x2: int, y2: int) -> bool:
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


def sign(a: int, b: int) -> int:
    return 1 if a > b else -1


def compute_segment_position(
    prev_segment_position: Position,
    segment_position: Position,
) -> Position:
    prev_x, prev_y = prev_segment_position
    seg_x, seg_y = segment_position

    if prev_x == seg_x and abs(prev_y - seg_y) == 2:
        seg_y += sign(prev_y, seg_y)
    elif prev_y == seg_y and abs(prev_x - seg_x) == 2:
        seg_x += sign(prev_x, seg_x)
    else:  # Diagonal
        seg_x += sign(prev_x, seg_x)
        seg_y += sign(prev_y, seg_y)

    return Position(seg_x, seg_y)


def simulate_movement(
    instructions: InputType,
    start_pos: Position = Position(0, 0),
    rope_length: int = 2,
) -> Dict[int, List[Position]]:
    out = {}
    for i in range(rope_length):
        out[i] = [start_pos]

    for (dx, dy), steps in instructions:
        for _ in range(steps):
            # Update head position
            out[0].append(Position(out[0][-1].x + dx, out[0][-1].y + dy))

            # Update segment positions
            for i in range(1, rope_length):
                if not is_adjacent(
                    x1=out[i - 1][-1].x,
                    y1=out[i - 1][-1].y,
                    x2=out[i][-1].x,
                    y2=out[i][-1].y,
                ):
                    x, y = compute_segment_position(
                        prev_segment_position=out[i - 1][-1],
                        segment_position=out[i][-1],
                    )
                else:
                    x, y = out[i][-1]

                out[i].append(Position(x, y))

    return out


def number_of_distinct_tail_positions(data: InputType, rope_length: int) -> int:
    positions = simulate_movement(instructions=data, rope_length=rope_length)

    return len(set(positions[rope_length - 1]))


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = number_of_distinct_tail_positions(data, rope_length=2)
        solution_two = number_of_distinct_tail_positions(data, rope_length=10)

        if path == "data/example.txt":
            assert solution_one == 13
            assert solution_two == 1

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
