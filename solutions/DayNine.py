import argparse
import pathlib
from typing import Iterator, List, Tuple


# TODO(brendes6): Extract to utilities
def data_reader(day: str, is_test: bool) -> Iterator[str]:
    path = pathlib.Path(__file__).parent
    if is_test:
        path = path.parent / "inputs" / "Test"
    else:
        path = path.parent / "inputs" / "Data"
    with open(path / f"Day{day.title()}") as f:
        for line in f:
            yield (line.rstrip("\n"))


def parse_data(data: Iterator[str]) -> Tuple[List[int], List[int]]:
    # only one line
    line = next(data)
    file_blks = list(map(int, line[0::2]))
    space_blks = list(map(int, line[1::2]))
    return file_blks, space_blks


def part_one(file_blks: List[int], space_blks: List[int]):
    mem_index = 0
    left_f_index = 0
    right_f_index = len(file_blks) - 1
    total_file_size = sum(file_blks)
    checksum = 0
    while mem_index < total_file_size:
        if file_blks[left_f_index] > 0:
            checksum += left_f_index * mem_index
            mem_index += 1
            file_blks[left_f_index] -= 1
        elif space_blks[left_f_index] > 0:
            checksum += right_f_index * mem_index
            mem_index += 1
            file_blks[right_f_index] -= 1
            space_blks[left_f_index] -= 1
            if file_blks[right_f_index] == 0:
                right_f_index -= 1
        else:
            left_f_index += 1

    return checksum


def part_two(file_blks: List[int], space_blks: List[int]):
    file_starts = dict()
    space_starts = dict()
    file_id = 0
    mem_index = 0
    for file_id in range(len(file_blks)):
        file_starts[file_id] = mem_index
        mem_index += file_blks[file_id]
        if file_id < len(space_blks):
            space_starts[file_id] = mem_index
            mem_index += space_blks[file_id]
    file_id = len(file_blks) - 1
    for n, file_size in enumerate(file_blks[::-1]):
        for i in range(len(space_blks)):
            if space_starts[i] > file_starts[file_id - n]:
                break
            if space_blks[i] >= file_size:
                space_blks[i] -= file_size
                file_starts[file_id - n] = space_starts[i]
                space_starts[i] += file_size
                break
    checksum = 0
    for n in range(len(file_blks)):
        file_size = file_blks[n]
        # sum of conecutive integers a to b formula:
        # (b - a + 1) * (b + a) / 2
        checksum += (file_size) * (2 * file_starts[n] + file_size - 1) // 2 * n
    return checksum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("nine", args.test)
    l = parse_data(dr)
    if args.one:
        print(part_one(*l))
    elif args.two:
        print(part_two(*l))
