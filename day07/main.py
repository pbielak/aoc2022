"""Day 7 - Advent of Code"""
from typing import Dict, List, NamedTuple, Optional


class File(NamedTuple):
    name: str
    size: int

    @classmethod
    def from_string(cls, raw: str) -> "File":
        size, name = raw.split(" ")

        return cls(name=name, size=int(size))


class Directory(NamedTuple):
    full_path: str
    parent_dir: Optional["Directory"]
    directories: Dict[str, "Directory"]
    files: List[File]

    def size(self) -> int:
        file_sizes = sum(file.size for file in self.files)
        subdir_sizes = sum(
            sub_directory.size()
            for sub_directory in self.directories.values()
        )

        return file_sizes + subdir_sizes

    def __repr__(self):
        parent_dir_path = (
            self.parent_dir.full_path
            if self.parent_dir is not None
            else None
        )
        return (
            f"Directory("
            f"full_path={self.full_path}, "
            f"parent={parent_dir_path}, "
            f"directories={self.directories}, "
            f"files={self.files})"
        )

    def __hash__(self) -> int:
        return hash(self.full_path)


InputType = Directory


def read_data(path: str) -> InputType:
    with open(path, "r") as fin:
        file_tree = Directory("/", None, {}, [])
        current_dir = file_tree

        for line in fin.read().split("$")[1:]:
            command, *output = line.lstrip().split("\n")

            if command.startswith("cd"):
                target_dir = command.replace("cd ", "")

                if target_dir == "/":
                    current_dir = file_tree
                elif target_dir == "..":
                    current_dir = current_dir.parent_dir
                else:
                    assert target_dir in current_dir.directories.keys()
                    current_dir = current_dir.directories[target_dir]
            elif command.startswith("ls"):
                for entry in output:
                    if entry == "":
                        continue
                    elif entry.startswith("dir"):
                        dir_name = entry.replace("dir ", "")

                        assert dir_name not in current_dir.directories.keys()

                        current_path = current_dir.full_path
                        if current_path == "/":
                            full_path = f"/{dir_name}"
                        else:
                            full_path = f"{current_path}/{dir_name}"

                        current_dir.directories[dir_name] = Directory(
                            full_path=full_path,
                            parent_dir=current_dir,
                            directories={},
                            files=[],
                        )
                    else:
                        current_dir.files.append(File.from_string(entry))
        return file_tree


def get_directory_sizes(file_tree: Directory) -> Dict[str, int]:
    sizes = {}

    def _collect(directory: Directory):
        sizes[directory.full_path] = directory.size()
        for name, sub_directory in directory.directories.items():
            _collect(sub_directory)

    _collect(file_tree)
    return sizes


def solve_part_one(data: InputType) -> int:
    directory_sizes = get_directory_sizes(data)

    return sum(size for size in directory_sizes.values() if size <= 100_000)


def solve_part_two(data: InputType) -> int:
    directory_sizes = get_directory_sizes(data)

    total_disk_space = 70_000_000
    required_space = 30_000_000
    current_free_space = total_disk_space - directory_sizes["/"]

    space_to_free = required_space - current_free_space

    return min(
        size
        for size in directory_sizes.values()
        if size >= space_to_free
    )


def main():
    for path in ("data/example.txt", "data/input.txt"):
        data = read_data(path)

        solution_one = solve_part_one(data)
        solution_two = solve_part_two(data)

        if path == "data/example.txt":
            assert solution_one == 95_437
            assert solution_two == 24_933_642

        print(
            f"File: {path}\n"
            f"* Part One: {solution_one}\n"
            f"* Part Two: {solution_two}\n"
        )


if __name__ == "__main__":
    main()
