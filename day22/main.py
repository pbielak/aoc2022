"""Day 22 - Advent of Code"""
from typing import List, Tuple, Union

Map = List[List[str]]
Instructions = List[Union[str, int]]
InputType = Tuple[Map, Instructions]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        _map, instructions = fin.read().split("\n\n")

        _map = [list(row) for row in _map.split("\n")]

        # Pad all lines to the same length
        max_len = max(len(row) for row in _map)
        _map = [row + [" "] * (max_len - len(row)) for row in _map]

        instructions = [
            i if i in ("L", "R") else int(i)
            for i in (
                instructions
                .replace("L", ",L,")
                .replace("R", ",R,")
                .split(",")
            )
        ]
        return _map, instructions


def solve_part_one(data: InputType) -> int:
    DIRECTION_UPDATE = {
        # Clockwise
        ("RIGHT", "R"): "DOWN",
        ("DOWN", "R"): "LEFT",
        ("LEFT", "R"): "UP",
        ("UP", "R"): "RIGHT",

        # Counterclockwise
        ("RIGHT", "L"): "UP",
        ("UP", "L"): "LEFT",
        ("LEFT", "L"): "DOWN",
        ("DOWN", "L"): "RIGHT",
    }

    DIRECTION_DELTA = {
        "RIGHT": (0, 1),
        "LEFT": (0, -1),
        "UP": (-1, 0),
        "DOWN": (1, 0),
    }

    _map, instructions = data

    # Start position and direction
    i, j = 0, _map[0].index(".")
    direction = "RIGHT"

    #print("Start:", i, j)
    for ins in instructions:
        if ins in ("L", "R"):
            direction = DIRECTION_UPDATE[(direction, ins)]
        else:
            di, dj = DIRECTION_DELTA[direction]
            next_i, next_j = i, j

            for _ in range(ins):
                finish_instruction = False

                while True:
                    next_i = (next_i + di) % len(_map)
                    next_j = (next_j + dj) % len(_map[0])

                    if _map[next_i][next_j] == " ":
                        continue

                    if _map[next_i][next_j] == ".":
                        break

                    if _map[next_i][next_j] == "#":
                        # Undo step(s)
                        while True:
                            next_i = (next_i - di) % len(_map)
                            next_j = (next_j - dj) % len(_map[0])

                            if _map[next_i][next_j] == ".":
                                break

                        finish_instruction = True
                        break

                if finish_instruction:
                    break

            i, j = next_i, next_j

        #print(ins, "=>", i, j)

    row = i + 1
    col = j + 1
    facing = ["RIGHT", "DOWN", "LEFT", "UP"].index(direction)

    answer = 1000 * row + 4 * col + facing

    return answer


def solve_part_two(data: InputType) -> int:
    pass


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 6_032
            #assert solution_two == ...

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
