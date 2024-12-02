import argparse
import pathlib
from typing import Iterator

def data_reader(day: str, is_test: bool) -> Iterator[str]:
    path = pathlib.Path(__file__).parent
    if is_test:
        path = path.parent/"inputs"/"Test"
    else:
        path = path.parent/"inputs"/"Data"
    with open(path/f"Day{day.title()}") as f:
        for line in f:
            yield(line.rstrip("\n"))

def parse_data(data_reader: Iterator[str]) -> tuple[list[int], list[int]]:
    l, r = list(), list()
    for line in data_reader:
        data = line.split()
        l.append(int(data[0]))
        r.append(int(data[1]))
    return l, r


def part_one(left: list[int], right: list[int]) -> int:
    # Brute force.  Sort lists and add the abs values
    # of the difference.
    _sort_l, _sort_r = sorted(left), sorted(right)
    return sum(abs(a - b) for a, b in zip(_sort_l, _sort_r))


def part_two(left: list[int], right: list[int]) -> int:
    counts = dict()
    for x in right:
        counts[x] = counts.get(x, 0) + 1
    return sum(a * counts.get(a, 0) for a in left)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("one", args.test)
    l, r = parse_data(dr)
    if args.one:
        print(part_one(l, r))
    elif args.two:
        print(part_two(l, r))
