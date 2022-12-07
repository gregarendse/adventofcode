#!/use/bin/env python
from dataclasses import dataclass
from sys import argv
from typing import List, Dict


def read_file(file: str) -> List[str]:
    with open(file, 'r') as f:
        return f.readlines()


@dataclass()
class File:
    name: str
    size: int


@dataclass
class Directory(object):
    name: str
    parent: object
    files: List[File]
    directories: Dict

    def size(self):
        return sum([f.size for f in self.files])


def calculate_sizes(directories: Directory) -> int:
    size: int = 0

    for k, v in directories.directories.items():
        size += calculate_sizes(v)

    return directories.size() + size


def find(directory: Directory) -> List[Directory]:
    directories: List[Directory] = []

    for k, v in directory.directories.items():
        directories.extend(find(v))

        size: int = calculate_sizes(v)
        if size <= 100000:
            directories.append(v)

    return directories


def find_greater(directory: Directory, minimum: int = 100000) -> List[Directory]:
    directories: List[Directory] = []

    size: int = calculate_sizes(directory)

    if size >= minimum:
        directories.append(directory)

    for k, v in directory.directories.items():
        directories.extend(find_greater(v, minimum))

    return directories


def part_one(file: str) -> int:
    lines: List[str] = read_file(file)

    root = get_directories(lines)

    dirs = find(root)

    return sum([calculate_sizes(x) for x in dirs])


def get_directories(lines: List[str]) -> Directory:
    directories: Directory = Directory("/", None, [], {})
    root: Directory = directories
    for line in lines:
        line = line.strip()
        if line.startswith("$"):
            #         command
            if line.startswith("$ cd .."):
                #     previous directory
                directories = directories.parent
            elif line.startswith("$ cd /"):
                directories = root
            elif line.startswith("$ cd "):
                #     new directory
                dir_name = line[5:]
                directories = directories.directories.get(dir_name)
        else:
            if line.startswith("dir "):
                #     directory
                dir_name = line[4:]
                directories.directories[dir_name] = Directory(dir_name, directories, [], {})
            else:
                #         file
                [size, name] = line.split(" ")
                directories.files.append(File(name, int(size)))
    return root


def part_two(file: str) -> int:
    lines: List[str] = read_file(file)
    root: Directory = get_directories(lines)

    total_space: int = 70000000
    required_space: int = 30000000
    current_usage: int = calculate_sizes(root)
    current_space: int = total_space - current_usage
    remove: int = required_space - current_space

    dirs = find_greater(root, remove)

    removable_size: int = total_space
    for d in dirs:
        size: int = calculate_sizes(d)
        if removable_size >= size >= remove:
            removable_size = size

    return removable_size


def main():
    print("Part One: {}".format(part_one(argv[1])))
    print("Part Two: {}".format(part_two(argv[1])))


if __name__ == '__main__':
    main()
