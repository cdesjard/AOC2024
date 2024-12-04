import pathlib
import argparse
from typing import Iterator
import re

PART_ONE_RE = re.compile(r"mul\((\d+),(\d+)\)")
PART_TWO_RE = re.compile(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))")


def data_reader(day: str, is_test: bool) -> Iterator[str]:
    path = pathlib.Path(__file__).parent
    if is_test:
        path = path.parent / "inputs" / "Test"
    else:
        path = path.parent / "inputs" / "Data"
    with open(path / f"Day{day.title()}") as f:
        for line in f:
            yield (line.rstrip("\n"))


def parse_data(data_reader: Iterator[str]) -> Iterator[str]:
    return data_reader


def part_one(lines: Iterator[str]) -> int:
    # There might be newlines, so the Iterator might have more than one line.  We should add the results
    total = 0
    for line in lines:
        pairs = PART_ONE_RE.findall(line)
        total += sum(int(a) * int(b) for a, b in pairs)
    return total


def part_two(lines: Iterator[str]) -> int:
    total = 0
    doing = True
    for line in lines:
        for a, b, do, dont in PART_TWO_RE.findall(line):
            if do:
                doing = True
            elif dont:
                doing = False
            elif doing:
                total += int(a) * int(b)
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("three", args.test)
    l = parse_data(dr)
    if args.one:
        print(part_one(l))
    elif args.two:
        print(part_two(l))
