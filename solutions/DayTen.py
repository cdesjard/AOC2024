import argparse
from dataclasses import dataclass
from enum import Enum
import pathlib
from typing import Iterator, List, Set, Tuple


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


def parse_data(data: Iterator[str]) -> List[List[int]]:
    map_data = list()
    for line in data:
        map_data.append(list(map(int, line)))
    return map_data


@dataclass
class DirectionMixin:
    y: int
    x: int


class Direction(DirectionMixin, Enum):
    N = -1, 0
    W = 0, -1
    E = 0, 1
    S = 1, 0


def solution_one(map_data: List[List[int]]) -> int:

    height = len(map_data)
    width = len(map_data[0])

    trailheads = list(
        (y, x) for x in range(width) for y in range(height) if map_data[y][x] == 0
    )

    def in_bounds(x: int, y: int) -> bool:
        return (0 <= x < width) and (0 <= y < height)

    def find_summits(x: int, y: int, dir: Direction) -> Set[Tuple[int, int]]:
        cur_alt = map_data[y][x]
        if in_bounds(x + dir.x, y + dir.y) and (
            map_data[y + dir.y][x + dir.x] - cur_alt == 1
        ):
            x += dir.x
            y += dir.y
            if map_data[y][x] == 9:
                return set({(y, x)})
            return set.union(*(find_summits(x, y, d) for d in Direction))
        return set()

    return sum(
        len(set.union(*(find_summits(x, y, d) for d in Direction)))
        for (y, x) in trailheads
    )


def solution_two(map_data: List[List[int]]) -> int:

    height = len(map_data)
    width = len(map_data[0])

    trailheads = list(
        (y, x) for x in range(width) for y in range(height) if map_data[y][x] == 0
    )

    def in_bounds(x: int, y: int) -> bool:
        return (0 <= x < width) and (0 <= y < height)

    def count_trails(x: int, y: int, dir: Direction) -> int:
        cur_alt = map_data[y][x]
        if in_bounds(x + dir.x, y + dir.y) and (
            map_data[y + dir.y][x + dir.x] - cur_alt == 1
        ):
            x += dir.x
            y += dir.y
            if map_data[y][x] == 9:
                return 1
            return sum(count_trails(x, y, d) for d in Direction)
        return 0

    return sum(count_trails(x, y, d) for (y, x) in trailheads for d in Direction)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("ten", args.test)
    l = parse_data(dr)
    if args.one:
        print(solution_one(l))
    elif args.two:
        print(solution_two(l))
