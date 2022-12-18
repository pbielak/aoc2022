"""Day 18 - Advent of Code"""
from typing import List, NamedTuple, Set


class Point3D(NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def from_string(cls, raw: str) -> "Point3D":
        x, y, z = raw.split(",")
        return cls(x=int(x), y=int(y), z=int(z))

    def neighbors(self) -> List["Point3D"]:
        return [
            Point3D(self.x, self.y, self.z + 1),
            Point3D(self.x, self.y, self.z - 1),
            Point3D(self.x, self.y + 1, self.z),
            Point3D(self.x, self.y - 1, self.z),
            Point3D(self.x + 1, self.y, self.z),
            Point3D(self.x - 1, self.y, self.z),
        ]


class ColoredPoint3D(Point3D):
    color: str

InputType = Set[Point3D]


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return {
            Point3D.from_string(line.strip())
            for line in fin.readlines()
        }


def solve_part_one(data: InputType) -> int:
    num_cubes = len(data)

    num_sides = num_cubes * 6

    for cube in data:
        n_neighbors = sum(neighbor in data for neighbor in cube.neighbors())

        num_sides -= n_neighbors

    return num_sides


def solve_part_two(data: InputType) -> int:
    # Find all air pockets – flood-fill/coloring method
    grid = set()
    colors = {}
    xs, ys, zs = zip(*data)

    for x in range(min(xs) - 1, max(xs) + 2):
        for y in range(min(ys) - 1, max(ys) + 2):
            for z in range(min(zs) - 1, max(zs) + 2):
                cube = Point3D(x, y, z)

                grid.add(cube)
                colors[cube] = "Lava" if cube in data else ""

    start_cube = Point3D(min(xs), min(ys), min(zs))
    assert start_cube not in data
    queue = [
        n
        for n in start_cube.neighbors()
        if n in grid
    ]
    while queue:
        cube = queue.pop(0)

        if colors[cube] in ("Lava", "Outside"):
            continue
        else:
            colors[cube] = "Outside"
            queue.extend([
                n
                for n in cube.neighbors()
                if n in grid
            ])

    num_sides = solve_part_one(data)
    not_visited = [k for k, v in colors.items() if v == ""]

    for cube in not_visited:
        for n in cube.neighbors():
            if n in data:
                num_sides -= 1

    return num_sides


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 64
            assert solution_two == 58

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
