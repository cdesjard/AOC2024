import argparse
import functools
import pathlib
from typing import Iterator, Tuple


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


def parse_data(data_reader: Iterator[str]) -> Tuple[list[Tuple[int]], list[list[int]]]:
    rules = list()
    for line in data_reader:
        if "|" in line:
            rules.append(tuple(map(int, line.split("|"))))
        else:
            break
    updates = list(list(map(int, line.split(","))) for line in data_reader)
    return rules, updates


def part_one(rules: list[Tuple[int]], updates: list[list[int]]):
    forbids_dict = dict()
    for a, b in rules:
        forbids_dict.setdefault(b, set()).add(a)
    total_sum = 0
    for update in updates:
        forbidden = set()
        good_update = True
        for x in update:
            if x in forbidden:
                good_update = False
                break
            forbidden.update(forbids_dict.get(x, set()))
        if good_update:
            total_sum += update[len(update) // 2]
    return total_sum


def part_two(rules: list[Tuple[int]], updates: list[list[int]]):
    bad_updates = list()
    forbids_dict = dict()
    for a, b in rules:
        forbids_dict.setdefault(b, set()).add(a)
    for update in updates:
        forbidden = set()
        for x in update:
            if x in forbidden:
                bad_updates.append(update)
                break
            forbidden.update(forbids_dict.get(x, set()))

    @functools.cmp_to_key
    def cmp_items(a, b):
        if (a, b) in rules:
            return -1
        elif (b, a) in rules:
            return 1
        return 0

    total_sum = 0
    for update in bad_updates:
        update.sort(key=cmp_items)
        total_sum += update[len(update) // 2]
    return total_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("five", args.test)
    if args.one:
        print(part_one(*parse_data(dr)))
    elif args.two:
        print(part_two(*parse_data(dr)))
