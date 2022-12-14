"""Day 14 - Advent of Code"""
from typing import List, Set, Tuple

Position = Tuple[int, int]
RockLine = List[Position]
InputType = List[RockLine]


def read_data(path: str) -> InputType:
    rock_lines = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            current_line = []
            for position in line.strip().split(" -> "):
                x, y = position.split(",")
                current_line.append((int(x), int(y)))
            rock_lines.append(current_line)
    return rock_lines


def generate_all_rock_positions(rock_lines: InputType) -> Set[Position]:
    positions = set()

    for rock_line in rock_lines:
        for (start_x, start_y), (end_x, end_y) in zip(rock_line, rock_line[1:]):
            if start_x == end_x:
                for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                    positions.add((start_x, y))
            else:
                assert start_y == end_y
                for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                    positions.add((x, start_y))

    return positions


def simulate(
    rock_positions: Set[Position],
    source_pos: Position = (500, 0),
    use_floor: bool = False,
) -> Set[Position]:
    sand_positions = set()

    max_rock_y = max(y for _, y in rock_positions)

    def _is_free(_x, _y):
        return all(
            (_x, _y) not in pos
            for pos in (rock_positions, sand_positions)
        ) and _y < max_rock_y + 2

    def _can_move_down(_x, _y):
        return _is_free(_x, _y + 1)

    def _can_move_down_left(_x, _y):
        return _is_free(_x - 1, _y + 1)

    def _can_move_down_right(_x, _y):
        return _is_free(_x + 1, _y + 1)

    def _update_pos(_x, _y) -> Position:
        if _can_move_down(_x, _y):
            return _x, _y + 1

        if _can_move_down_left(_x, _y):
            return _x - 1, _y + 1

        if _can_move_down_right(x, y):
            return _x + 1, _y + 1

        return _x, _y

    while True:
        x, y = source_pos

        while True:
            new_x, new_y = _update_pos(x, y)

            if use_floor:
                if (new_x, new_y) == source_pos:
                    return sand_positions
            else:
                if new_y > max_rock_y:  # Falls below last rock into abyss
                    return sand_positions

            if (new_x, new_y) == (x, y):
                sand_positions.add((new_x, new_y))
                break

            x, y = new_x, new_y


def solve_part_one(data: InputType) -> int:
    rock_pos = generate_all_rock_positions(rock_lines=data)
    sand_pos = simulate(rock_positions=rock_pos)

    return len(sand_pos)


def solve_part_two(data: InputType) -> int:
    rock_pos = generate_all_rock_positions(rock_lines=data)
    sand_pos = simulate(rock_positions=rock_pos, use_floor=True)

    return len(sand_pos) + 1


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 24
            assert solution_two == 93

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
