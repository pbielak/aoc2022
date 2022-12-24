"""Day 21 - Advent of Code"""
from typing import Dict, Tuple

InputType = Dict[str, str]


class ExprOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self) -> int:
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.evaluate()

        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.evaluate()

        return self._op(left, right)

    def _op(self, a: int, b: int) -> int:
        pass

    def inverse(self, value: int) -> Tuple[int, "ExprOp"]:
        left, right = self.left, self.right

        try:
            left = left.evaluate()
        except AttributeError:
            pass

        try:
            right = right.evaluate()
        except AttributeError:
            pass

        if isinstance(left, int):
            return self._inv_op(value, left, pos="left"), right
        elif isinstance(right, int):
            return self._inv_op(value, right, pos="right"), left
        else:
            raise RuntimeError(f"No idea how this happened: {self}")

    def _inv_op(self, target: int, arg: int, pos: str) -> int:
        pass


class Add(ExprOp):
    def _op(self, a: int, b: int) -> int:
        return a + b

    def _inv_op(self, target: int, arg: int, pos: str) -> int:
        return target - arg

    def __repr__(self):
        return f"({self.left} + {self.right})"


class Sub(ExprOp):
    def _op(self, a: int, b: int) -> int:
        return a - b

    def _inv_op(self, target: int, arg: int, pos: str) -> int:
        if pos == "left":
            return arg - target
        elif pos == "right":
            return target + arg
        else:
            raise RuntimeError(f"Inv: No idea how this happened: {self}")

    def __repr__(self):
        return f"({self.left} - {self.right})"


class Mul(ExprOp):
    def _op(self, a: int, b: int) -> int:
        return a * b

    def _inv_op(self, target: int, arg: int, pos: str) -> int:
        return target // arg

    def __repr__(self):
        return f"({self.left} * {self.right})"


class Div(ExprOp):
    def _op(self, a: int, b: int) -> int:
        return a // b

    def _inv_op(self, target: int, arg: int, pos: str) -> int:
        if pos == "left":
            return arg // target
        elif pos == "right":
            return target * arg
        else:
            raise RuntimeError(f"Inv: No idea how this happened: {self}")

    def __repr__(self):
        return f"({self.left} / {self.right})"


def read_data(path: str) -> InputType:
    monkeys = {}
    with open(path, "r") as fin:
        for line in fin.readlines():
            name, expr = line.strip().split(": ")
            monkeys[name] = expr
    return monkeys


def build_expression(monkeys: InputType, key: str) -> str:
    expr_parts = monkeys[key].split(" ")

    if len(expr_parts) == 1:  # Number
        return expr_parts[0]

    # Expression
    left = build_expression(monkeys, key=expr_parts[0])
    op = expr_parts[1].replace("/", "//")
    right = build_expression(monkeys, key=expr_parts[2])

    expr = f"({left} {op} {right})"

    if "humn" not in expr:
        return str(eval(expr))

    return expr


def solve_part_one(data: InputType) -> int:
    full_expr = build_expression(monkeys=data, key="root")
    return eval(full_expr)


def build_expression_2(monkeys: InputType, key: str) -> ExprOp:
    expr_parts = monkeys[key].split(" ")

    if len(expr_parts) == 1:  # Number
        num = expr_parts[0]

        if num == "humn":
            return num

        return int(num)

    # Expression
    left = build_expression_2(monkeys, key=expr_parts[0])
    op = expr_parts[1]
    right = build_expression_2(monkeys, key=expr_parts[2])

    OPS = {"+": Add, "-": Sub, "*": Mul, "/": Div}
    return OPS[op](left, right)


def solve_part_two(data: InputType) -> int:
    data = data.copy()
    data["humn"] = "humn"
    left_monkey, _, right_monkey = data["root"].split(" ")

    expr = build_expression_2(monkeys=data, key=left_monkey)
    target_value = build_expression_2(monkeys=data, key=right_monkey).evaluate()

    humn = target_value

    while expr != "humn":
        humn, expr = expr.inverse(value=humn)

    return humn


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 152
            assert solution_two == 301

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
