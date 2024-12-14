import argparse
import functools
import pathlib
from typing import Iterator


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


def parse_data(data: Iterator[str]) -> list[str]:
    # Should only be one line
    return next(data).split()


def solution(start_data: list[str], num_blinks: int = 75) -> int:

    @functools.lru_cache(maxsize=1024 * 1024)
    def evolve(x: int, steps_left: int) -> int:
        if steps_left == 0:
            return 1
        x_s = str(x)
        if x == 0:
            return evolve(1, steps_left - 1)
        else:
            if len(x_s) % 2 == 0:
                return evolve(int(x_s[: len(x_s) // 2]), steps_left - 1) + evolve(
                    int(x_s[len(x_s) // 2 :]), steps_left - 1
                )
            else:
                return evolve(2024 * x, steps_left - 1)

    return sum(evolve(int(n), num_blinks) for n in start_data)


def solution_one(start_data: list[str]) -> int:
    return solution(start_data, 25)


def solution_two(start_data: list[str]) -> int:
    return solution(start_data, 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("eleven", args.test)
    l = parse_data(dr)
    if args.one:
        print(solution_one(l))
    elif args.two:
        print(solution_two(l))
