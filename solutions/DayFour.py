import argparse
from dataclasses import dataclass
from enum import Enum
import pathlib
from typing import ClassVar, Iterator, Tuple


def data_reader(day: str, is_test: bool) -> Iterator[str]:
    path = pathlib.Path(__file__).parent
    if is_test:
        path = path.parent / "inputs" / "Test"
    else:
        path = path.parent / "inputs" / "Data"
    with open(path / f"Day{day.title()}") as f:
        for line in f:
            yield (line.rstrip("\n"))


def parse_data(data_reader: Iterator[str]) -> list[str]:
    return list(r for r in data_reader)


class GameBoard:

    # Directions
    @dataclass
    class DirectionMixin:
        r: int
        c: int

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

    def has_word_at(self, word: str, direction: Direction, r: int = 0, c: int = 0):

        if len(word) == 0:
            return True
        if not (0 <= r < self._length) or not (0 <= c < self._width):
            return False
        if self._data[r][c] != word[0]:
            return False
        r += direction.r
        c += direction.c
        return self.has_word_at(word[1:], direction, r, c)

    def count_word(self, word: str):

        if len(word) == 0:
            raise Exception("Zero length word provided")
        count = 0
        for r in range(self._width):
            for c in range(self._length):
                for direction in GameBoard.Direction:
                    if self.has_word_at(word, direction, r, c):
                        count += 1
        return count

    def count_x_mas(self):
        count = 0
        for r in range(1, self._length - 1):
            for c in range(1, self._width - 1):
                if self._data[r][c] != "A":
                    continue
                l_diag = (
                    self._data[r + GameBoard.Direction.NW.r][
                        c + GameBoard.Direction.NW.c
                    ],
                    self._data[r + GameBoard.Direction.SE.r][
                        c + GameBoard.Direction.SE.c
                    ],
                )
                r_diag = (
                    self._data[r + GameBoard.Direction.SW.r][
                        c + GameBoard.Direction.SW.c
                    ],
                    self._data[r + GameBoard.Direction.NE.r][
                        c + GameBoard.Direction.NE.c
                    ],
                )
                if l_diag in (("M", "S"), ("S", "M")) and r_diag in (
                    ("M", "S"),
                    ("S", "M"),
                ):
                    count += 1
        return count


def part_one(rows: list[str]) -> int:
    g = GameBoard(rows)
    return g.count_word("XMAS")


def part_two(rows: list[str]) -> int:
    g = GameBoard(rows)
    return g.count_x_mas()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("four", args.test)
    d = parse_data(dr)
    if args.one:
        print(part_one(d))
    elif args.two:
        print(part_two(d))
