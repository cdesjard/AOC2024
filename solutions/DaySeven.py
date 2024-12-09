import argparse
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


def parse_data(data: Iterator[str]) -> Iterator[Tuple[int, list[int]]]:
    for line in data:
        data = line.split(":")
        yield int(data[0]), list(map(int, data[1].strip().split()))


def part_one(test_cases: Iterator[Tuple[int, list[int]]]) -> int:

    # DFS
    def dfs(target, num_list, val):
        if len(num_list) == 0:
            return target == val
        else:
            for i, x in enumerate(num_list):
                return dfs(target, num_list[:i] + num_list[i + 1 :], val * x) or dfs(
                    target, num_list[:i] + num_list[i + 1 :], val + x
                )

    total = 0
    for solution, operands in test_cases:
        # DFS
        if dfs(solution, operands, 0):
            total += solution
    return total


def part_two(test_cases: Iterator[Tuple[int, list[int]]]) -> int:

    # DFS Again, but break if big; these operators only grow
    def dfs(target, num_list, val):
        if len(num_list) == 0:
            return target == val
        elif val > target:
            return False
        else:
            for i, x in enumerate(num_list):
                return (
                    dfs(target, num_list[:i] + num_list[i + 1 :], val * x)
                    or dfs(target, num_list[:i] + num_list[i + 1 :], val + x)
                    or dfs(
                        target, num_list[:i] + num_list[i + 1 :], int(str(val) + str(x))
                    )
                )

    total = 0
    for solution, operands in test_cases:
        # DFS
        if dfs(solution, operands, 0):
            total += solution
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("seven", args.test)
    if args.one:
        print(part_one(parse_data(dr)))
    elif args.two:
        print(part_two(parse_data(dr)))
