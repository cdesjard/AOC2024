import argparse
import itertools
from math import gcd
import pathlib
from typing import Dict, Iterator, Set, Tuple


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


def parse_data(data: Iterator[str]) -> Tuple[int, int, Dict[str, Set[Tuple[int]]]]:
    antennas = dict()
    width = None
    height = 0
    for line in data:

        if width is None:
            width = len(line)
        else:
            assert width == len(line)
        for c, x in enumerate(line):
            if x == ".":
                continue
            else:
                antennas.setdefault(x, set()).add((height, c))
        height += 1
    return height, width, antennas


class AntennaBoard:

    def __init__(self, height: int, width: int, antennas: Dict[str, Set[Tuple[int]]]):
        self.height = height
        self.width = width
        self.antennas = antennas
        self.antinodes = set()

    def set_antinodes(self) -> None:
        self.antinodes = set()
        for k, v_set in self.antennas.items():
            for p_a, p_b in itertools.combinations(v_set, 2):
                r = 2 * p_b[0] - p_a[0]
                c = 2 * p_b[1] - p_a[1]
                if (0 <= r < self.height) and (0 <= c < self.width):
                    self.antinodes.add((r, c))
                r = 2 * p_a[0] - p_b[0]
                c = 2 * p_a[1] - p_b[1]
                if (0 <= r < self.height) and (0 <= c < self.width):
                    self.antinodes.add((r, c))

    def set_harmonic_antinodes(self) -> None:
        self.antinodes = set()
        for k, v_set in self.antennas.items():
            for p_a, p_b in itertools.combinations(v_set, 2):
                y_dist = p_a[0] - p_b[0]
                x_dist = p_a[1] - p_b[1]
                div = gcd(abs(x_dist), abs(y_dist))
                y_delta = y_dist / div
                x_delta = x_dist / div
                d = 0
                y, x = p_a
                while (0 <= y < self.height) and (0 <= x < self.width):
                    self.antinodes.add((y, x))
                    y += y_delta
                    x += x_delta
                y, x = p_a
                while (0 <= y < self.height) and (0 <= x < self.width):
                    self.antinodes.add((y, x))
                    y -= y_delta
                    x -= x_delta

    def __str__(self) -> str:
        line = ""

        def find_antenna(row: int, col: int) -> str | None:
            for k, s in self.antennas.items():
                if (r, c) in s:
                    return k
            return None

        for r in range(self.height):
            for c in range(self.width):
                k = find_antenna(r, c)
                if k:
                    line += k
                elif (r, c) in self.antinodes:
                    line += "#"
                else:
                    line += "."
            line += "\n"
        return line


def part_one(height: int, width: int, antennas: Dict[str, Tuple[int]]) -> int:
    board = AntennaBoard(height, width, antennas)
    board.set_antinodes()
    return len(board.antinodes)


def part_two(height: int, width: int, antennas: Dict[str, Tuple[int]]) -> int:
    board = AntennaBoard(height, width, antennas)
    board.set_harmonic_antinodes()
    return len(board.antinodes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("eight", args.test)
    if args.one:
        print(part_one(*parse_data(dr)))
    elif args.two:
        print(part_two(*parse_data(dr)))
