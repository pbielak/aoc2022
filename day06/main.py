"""Day 6 - Advent of Code"""
InputType = str


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        return fin.read()


def find_idx_of_start_marker(data: InputType, seq_len: int = 4) -> int:
    for i in range(seq_len, len(data)):
        if len(set(data[i - seq_len:i])) == seq_len:
            return i


def main():
    msg = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    assert find_idx_of_start_marker(msg, seq_len=4) == 7
    assert find_idx_of_start_marker(msg, seq_len=14) == 19

    msg = "bvwbjplbgvbhsrlpgdmjqwftvncz"
    assert find_idx_of_start_marker(msg, seq_len=4) == 5
    assert find_idx_of_start_marker(msg, seq_len=14) == 23

    msg = "nppdvjthqldpwncqszvftbrmjlhg"
    assert find_idx_of_start_marker(msg, seq_len=4) == 6
    assert find_idx_of_start_marker(msg, seq_len=14) == 23

    msg = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
    assert find_idx_of_start_marker(msg, seq_len=4) == 10
    assert find_idx_of_start_marker(msg, seq_len=14) == 29

    msg = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    assert find_idx_of_start_marker(msg, seq_len=4) == 11
    assert find_idx_of_start_marker(msg, seq_len=14) == 26

    for path in ("data/input.txt",):
        data = read_data(path)

        solution_one = find_idx_of_start_marker(data, seq_len=4)
        solution_two = find_idx_of_start_marker(data, seq_len=14)

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
