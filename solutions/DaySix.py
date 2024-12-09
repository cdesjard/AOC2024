import argparse
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from operator import add
import pathlib
from typing import Iterator, Self, Tuple


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


class GuardRoute:

    # Directions
    @dataclass
    class DirectionMixin:
        y: int
        x: int

    class Direction(DirectionMixin, Enum):
        N = -1, 0
        W = 0, -1
        E = 0, 1
        S = 1, 0

        def __hash__(self) -> int:
            return hash(repr(self))

    def __init__(
        self,
        length: int,
        width: int,
        obstacles: list[Tuple[int]],
        guard_start: Tuple[int],
        direction: Direction,
    ):
        self._length = length
        self._width = width
        self._obstacles = obstacles
        self._guard_loc = guard_start
        self._guard_dir = direction
        self._guard_out = False
        self._visited = set({self._guard_loc})
        self._states = set({(self._guard_loc, self._guard_dir)})

    def turn_guard(self) -> None:
        if self._guard_dir == GuardRoute.Direction.N:
            self._guard_dir = GuardRoute.Direction.E
        elif self._guard_dir == GuardRoute.Direction.E:
            self._guard_dir = GuardRoute.Direction.S
        elif self._guard_dir == GuardRoute.Direction.S:
            self._guard_dir = GuardRoute.Direction.W
        elif self._guard_dir == GuardRoute.Direction.W:
            self._guard_dir = GuardRoute.Direction.N
        else:
            raise Exception("Unknown Direction")

    def try_move(self) -> bool:
        if self._guard_out:
            return False
        new_loc = tuple(
            map(add, self._guard_loc, (self._guard_dir.y, self._guard_dir.x))
        )
        if new_loc in self._obstacles:
            self.turn_guard()
        else:
            self._guard_loc = new_loc
        # print(f"{self}")
        if new_loc[0] >= self._width or new_loc[0] < 0:
            self._guard_out = True
            return False
        if new_loc[1] >= self._length or new_loc[1] < 0:
            self._guard_out = True
            return False
        if (self._guard_loc, self._guard_dir) in self._states:
            return False
        self._visited.add(self._guard_loc)
        self._states.add((self._guard_loc, self._guard_dir))
        return True

    def run_guard(self) -> None:
        while self.try_move():
            pass
        # print(f"{self}")

    def get_num_visited(self) -> int:
        return len(self._visited)

    def add_obstacle(self, new_loc: Tuple[int]) -> None:
        if new_loc == self._guard_loc:
            raise Exception("Can't add obstacle on top of Guard")
        self._obstacles.append(new_loc)

    def __deepcopy__(self, memo: dict | None = None) -> Self:
        if self._guard_out:
            raise Exception("Can't copy GuardRoute after Guard leaves")
        return GuardRoute(
            self._length,
            self._width,
            deepcopy(self._obstacles, memo),
            deepcopy(self._guard_loc, memo),
            self._guard_dir,
        )

    def __str__(self) -> str:
        final = ""
        for r in range(self._length):
            line = ""
            for c in range(self._width):
                if (r, c) in self._visited:
                    line += "X"
                elif (r, c) in self._obstacles:
                    line += "#"
                elif (r, c) == self._guard_loc:
                    if self._guard_dir == GuardRoute.Direction.N:
                        line += "^"
                    elif self._guard_dir == GuardRoute.Direction.E:
                        line += ">"
                    elif self._guard_dir == GuardRoute.Direction.S:
                        line += "v"
                    elif self._guard_dir == GuardRoute.Direction.W:
                        line += "<"
                else:
                    line += "."
            final += line + "\n"
        return final


def parse_data(data_reader: Iterator[str]) -> GuardRoute:
    obstacles = list()
    guard_loc = None
    guard_dir = None
    row = 0
    for line in data_reader:
        for c, x in enumerate(line):
            if x == "#":
                obstacles.append((row, c))
            elif x == ".":
                continue
            elif x in ("v", "<", ">", "^"):
                guard_loc = (row, c)
                if x == "v":
                    guard_dir = GuardRoute.Direction.S
                elif x == "<":
                    guard_dir = GuardRoute.Direction.W
                elif x == ">":
                    guard_dir = GuardRoute.Direction.E
                elif x == "^":
                    guard_dir = GuardRoute.Direction.N
        row += 1
    return GuardRoute(c + 1, row, obstacles, guard_loc, guard_dir)


def part_one(g: GuardRoute) -> int:
    g.run_guard()
    return g.get_num_visited()


def part_two(g: GuardRoute) -> int:
    # This is lame, don't want to copy lots of GuardRoutes
    good_spots = 0
    for r in range(g._length):
        for c in range(g._width):
            # print(f"Trying {(r,c)} of {(g._length, g._width)}")
            new_g = deepcopy(g)
            try:
                new_g.add_obstacle((r, c))
            except Exception as e:
                # print(str(e))
                continue
            new_g.run_guard()
            if not (new_g._guard_out):
                good_spots += 1
    return good_spots


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("six", args.test)
    if args.one:
        print(part_one(parse_data(dr)))
    elif args.two:
        print(part_two(parse_data(dr)))
