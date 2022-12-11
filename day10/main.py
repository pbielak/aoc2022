"""Day 10 - Advent of Code"""
from typing import List, Tuple, Optional

InputType = List[Tuple[str, Optional[int]]]


def read_data(path: str) -> InputType:
    instructions = []
    with open(path, "r") as fin:
        for line in fin.read().split("\n"):
            if line.startswith("addx"):
                instructions.append(("addx", int(line.split(" ")[1])))
            else:
                instructions.append(("noop", None))
    return instructions


def run_program(instructions: InputType) -> List[int]:
    register_x_states = [1]
    register_x = 1
    for instruction, argument in instructions:
        if instruction == "addx":
            register_x_states.append(register_x)
            register_x_states.append(register_x + argument)
            register_x += argument
        else:
            assert instruction == "noop"
            register_x_states.append(register_x)

    return register_x_states


def solve_part_one(data: InputType) -> int:
    register_x_states = run_program(instructions=data)

    answer = sum(
        cycle * register_x_states[cycle - 1]
        for cycle in (20, 60, 100, 140, 180, 220)
    )
    return answer


def solve_part_two(data: InputType, display_width: int = 40) -> str:
    crt_lines = []

    register_x_states = run_program(instructions=data)

    for idx in range(0, len(register_x_states) - 1, display_width):
        line = ""
        for cycle, x in enumerate(register_x_states[idx:idx + display_width]):
            if cycle in (x - 1, x, x + 1):
                line += "#"
            else:
                line += "."

        crt_lines.append(line)

    answer = "\n".join(crt_lines)
    return answer


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 13_140
            assert solution_two == (
                "##..##..##..##..##..##..##..##..##..##..\n"
                "###...###...###...###...###...###...###.\n"
                "####....####....####....####....####....\n"
                "#####.....#####.....#####.....#####.....\n"
                "######......######......######......####\n"
                "#######.......#######.......#######....."
            )

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: \n{solution_two}\n"
        )


if __name__ == "__main__":
    main()
