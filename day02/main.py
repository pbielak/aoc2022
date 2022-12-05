"""Day 2 - Advent of Code"""
from typing import List, Tuple

InputType = List[Tuple[str, str]]
SHAPE_SCORES = {"Rock": 1, "Paper": 2, "Scissors": 3}


def read_data(path: str) -> InputType:
    data = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            left, right = line.strip().split(" ")
            data.append((left, right))

    return data


def compute_outcome_score(opponent_move: str, my_move: str) -> int:
    if opponent_move == my_move:  # Draw
        return 3

    if (
        (opponent_move == "Rock" and my_move == "Scissors")
        or (opponent_move == "Scissors" and my_move == "Paper")
        or (opponent_move == "Paper" and my_move == "Rock")
    ):  # Defeated
        return 0

    return 6


def solve_part_one(data: InputType) -> int:
    move_decoder = {
        "A": "Rock", "B": "Paper", "C": "Scissors",
        "X": "Rock", "Y": "Paper", "Z": "Scissors",
    }

    game_score = 0
    for encoded_opponent_move, encoded_my_move in data:
        opponent_move = move_decoder[encoded_opponent_move]
        my_move = move_decoder[encoded_my_move]

        round_score = compute_outcome_score(
            opponent_move=opponent_move,
            my_move=my_move,
        ) + SHAPE_SCORES[my_move]

        game_score += round_score

    return game_score


def find_move(opponent_move: str, outcome: str) -> str:
    winning_moves = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}

    if outcome == "X":  # Need to lose
        return {v: k for k, v in winning_moves.items()}[opponent_move]
    elif outcome == "Y":  # Need to draw
        return opponent_move
    else:
        assert outcome == "Z"  # Need to win
        return winning_moves[opponent_move]


def solve_part_two(data: InputType) -> int:
    move_decoder = {"A": "Rock", "B": "Paper", "C": "Scissors"}

    game_score = 0
    for encoded_opponent_move, expected_outcome  in data:
        opponent_move = move_decoder[encoded_opponent_move]
        my_move = find_move(
            opponent_move=opponent_move,
            outcome=expected_outcome,
        )

        round_score = compute_outcome_score(
            opponent_move=opponent_move,
            my_move=my_move,
        ) + SHAPE_SCORES[my_move]

        game_score += round_score

    return game_score


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
