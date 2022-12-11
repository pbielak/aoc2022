"""Day 11 - Advent of Code"""
from collections import defaultdict
from copy import deepcopy
from typing import Dict, List, Tuple


class Monkey:

    def __init__(self, raw: str):
        _, items, update, test, pos, neg = raw.split("\n")

        self.items = [
            int(item)
            for item in (
                items
                .strip()
                .replace("Starting items: ", "")
                .replace(" ", "")
                .split(",")
            )
        ]
        self.update_fn = update.strip().replace("Operation: new = ", "")
        self.divisibility_factor = int(
            test.strip().replace("Test: divisible by ", "")
        )
        self.pos_destination = int(
            pos.strip().replace("If true: throw to monkey ", "")
        )
        self.neg_destination = int(
            neg.strip().replace("If false: throw to monkey ", "")
        )
        self.divisibility_factors_product = None

    def play(self, relief_factor: int = 3) -> Tuple[Dict[int, List[int]], int]:
        target_monkeys = defaultdict(list)
        num_inspections = len(self.items)

        for item in self.items:
            new_worry_level = eval(self.update_fn.replace("old", str(item)))
            new_worry_level //= relief_factor

            if new_worry_level % self.divisibility_factor == 0:
                destination = self.pos_destination
            else:
                destination = self.neg_destination

            target_monkeys[destination].append(
                new_worry_level % self.divisibility_factors_product
            )

        self.items = []
        return target_monkeys, num_inspections


InputType = List[Monkey]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        monkeys = [
            Monkey(description)
            for description in fin.read().split("\n\n")
        ]

        factor_product = 1

        for monkey in monkeys:
            factor_product *= monkey.divisibility_factor

        for monkey in monkeys:
            monkey.divisibility_factors_product = factor_product

        return monkeys


def execute_game(
    monkeys: InputType,
    num_rounds: int,
    relief_factor: int,
) -> int:
    scores = [0] * len(monkeys)

    for _ in range(1, num_rounds + 1):
        for idx, monkey in enumerate(monkeys):
            targets, num_inspections = monkey.play(relief_factor=relief_factor)

            for target_idx, new_items in targets.items():
                monkeys[target_idx].items.extend(new_items)

            scores[idx] += num_inspections

    top_scores = sorted(scores, reverse=True)
    answer = top_scores[0] * top_scores[1]
    return answer


def solve_part_one(data: InputType) -> int:
    return execute_game(
        monkeys=deepcopy(data),
        num_rounds=20,
        relief_factor=3,
    )


def solve_part_two(data: InputType) -> int:
    return execute_game(
        monkeys=deepcopy(data),
        num_rounds=10_000,
        relief_factor=1,
    )


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 10_605
            assert solution_two == 2_713_310_158

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
