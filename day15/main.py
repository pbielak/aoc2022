"""Day 15 - Advent of Code"""
from typing import List, NamedTuple, Set, Tuple


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, raw: str) -> "Point":
        x, y = raw.split(",")
        return cls(x=int(x), y=int(y))

    def manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


InputType = List[Tuple[Point, Point]]


def read_data(path: str) -> InputType:
    out = []
    with open(path, "r") as fin:
        for line in fin.readlines():
            sensor, beacon = (
                line
                .strip()
                .replace("Sensor at ", "")
                .replace(": closest beacon is at", "")
                .replace("x=", "")
                .replace("y=", "")
                .replace(", ", ",")
                .split(" ")
            )

            out.append((Point.from_string(sensor), Point.from_string(beacon)))

    return out


def get_impossible_positions_at_y(data: InputType, y: int) -> Set[int]:
    impossible_x_values = set()

    for sensor, beacon in data:
        dist = sensor.manhattan(beacon)
        y_diff = abs(sensor.y - y)

        if y_diff > dist:
            continue

        for x in range(
            sensor.x - (dist - y_diff),
            sensor.x + (dist - y_diff) + 1,
        ):
            if beacon.x == x and beacon.y == y:
                continue

            if sensor.x == x and sensor.y == y:
                continue

            impossible_x_values.add(x)

    return impossible_x_values


def find_distress_beacon_frequency(
    data: InputType,
    coordinate_min: int,
    coordinate_max: int,
) -> int:
    data_precomputed = [
        (sensor.x, sensor.y, sensor.manhattan(beacon))
        for sensor, beacon in data
    ]

    for sensor_x, sensor_y, dist in data_precomputed:
        dist = dist + 1

        for d in range(dist + 1):
            for obp_x, obp_y in [
                (sensor_x + d, sensor_y + dist - d),
                (sensor_x + d, sensor_y - (dist - d)),
                (sensor_x - d, sensor_y + dist - d),
                (sensor_x - d, sensor_y - (dist - d)),
            ]:
                if obp_x < coordinate_min or obp_x > coordinate_max:
                    continue

                if obp_y < coordinate_min or obp_y > coordinate_max:
                    continue

                if any(
                    abs(o_sensor_x - obp_x) + abs(o_sensor_y - obp_y) <= o_dist
                    for o_sensor_x, o_sensor_y, o_dist in data_precomputed
                ):
                    continue

                return obp_x * 4_000_000 + obp_y


def main():
    data = read_data("data/example.txt")
    assert len(get_impossible_positions_at_y(data, y=10)) == 26
    assert find_distress_beacon_frequency(
        data=data,
        coordinate_min=0,
        coordinate_max=20,
    ) == 56_000_011

    for path in ("data/input.txt",):
        data = read_data(path)

        solution_one = len(get_impossible_positions_at_y(data, y=2_000_000))

        solution_two = find_distress_beacon_frequency(
            data=data,
            coordinate_min=0,
            coordinate_max=4_000_000,
        )

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
