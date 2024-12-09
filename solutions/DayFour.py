import argparse
from dataclasses import dataclass
from enum import Enum
import pathlib
from typing import ClassVar, Iterator, Tuple

def data_reader(day: str, is_test: bool) -> Iterator[str]:
    path = pathlib.Path(__file__).parent
    if is_test:
        path = path.parent/"inputs"/"Test"
    else:
        path = path.parent/"inputs"/"Data"
    with open(path/f"Day{day.title()}") as f:
        for line in f:
            yield(line.rstrip("\n"))

def parse_data(data_reader: Iterator[str]) -> list[str]:
    return list(r for r in data_reader)


class GameBoard:

    # Directions 
    @dataclass
    class DirectionMixin:
        x: int
        y: int

    class Direction(DirectionMixin, Enum):
        NW = -1, -1
        N = -1, 0
        NE = -1, 1
        W = 0, -1
        E = 0, 1
        SW = 1, -1
        S = 1, 0
        SE = 1, 1





    def __init__(self, data: list[str]):
        self._data: list[str] = data
        if not self.validate_data():
            raise Exception("Data for GameBoard is invalid")
        self._length = len(self._data)
        self._width = len(self._data[0])

    def validate_data(self):
        if len(self._data) == 0:
            return False
        width = len(self._data[0])
        return all(len(r) == width for r in self._data)

    def count_word(self, word: str, r: int = 0, c: int = 0, direction: Direction|None = None):
        if len(word) == 0:
            return 1
        count = 0
        if 
                if c == word[0]:
                    if direction:
                        count += self.count_word(word[1:], direction)
                    else:
                        for direction in GameBoard.Direction:
                            count += self.count_word(word[1:], direction)
        return 






def part_one(rows: list[str]) -> int:
    count = 0
    for i, row in enumerate(rows):
        for j, c in row:
            if c = 'X':
                # Check all directions for 'XMAS'

            
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
