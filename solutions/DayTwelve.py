import argparse
from dataclasses import dataclass
from enum import Enum
import pathlib
from typing import Iterator, List, Self


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


def parse_data(data: Iterator[str]) -> List[List[str]]:
    return list(list(x for x in line) for line in data)


@dataclass(frozen=True)
class DirectionMixin:
    x: int
    y: int


class Direction(DirectionMixin, Enum):
    N = 0, -1
    W = -1, 0
    E = 1, 0
    S = 0, 1


class Plot:

    def __init__(self, crop: str):
        self.crop = crop
        self.region = None
        self.neighbors = dict({d: None for d in Direction})
        self.fences = dict({d: None for d in Direction})

    def shares_region(self, other: Self | None) -> bool:
        if other is None:
            return False
        return (self.region is not None) and self.region == other.region


class Field:

    class Region:

        def __init__(self):
            self.crop = None
            self.plots = set()
            self.fence_lines = 0

        def add_plot(self, plot: Plot) -> None:
            self.plots.add(plot)

        def get_area(self) -> int:
            return len(self.plots)

        def get_fence_cost(self) -> int:
            fences = 0
            for plot in self.plots:
                for n in plot.neighbors.values():
                    if n is None or n.region != self:
                        fences += 1
            return self.get_area() * fences

    def __init__(self, crops: List[List[str]]):
        self.height = len(crops)
        self.width = len(crops[0])
        self.plots = list()
        for row in crops:
            assert len(row) == self.width
            self.plots.append(list(Plot(crop) for crop in row))
        for y in range(self.height):
            for x in range(self.width):
                plot = self.plots[y][x]
                for d in Direction:
                    if self.in_bounds(x + d.x, y + d.y):
                        plot.neighbors[d] = self.plots[y + d.y][x + d.x]
        self.regions = set()

    def in_bounds(self, x: int, y: int) -> bool:
        return (0 <= x < self.width) and (0 <= y < self.height)

    def fill_regions(self) -> None:
        assert len(self.regions) == 0, "Already filled regions"
        region = Field.Region()
        for y in range(self.height):
            for x in range(self.width):
                plot = self.plots[y][x]
                if plot.region is not None:
                    continue
                self.fill_region(x, y, region)
                self.regions.add(region)
                region = Field.Region()

    def fill_region(self, x: int, y: int, region: Region) -> None:
        plot = self.plots[y][x]
        if plot.region is not None:
            return
        if region.crop is None:
            region.crop = plot.crop
        if plot.crop != region.crop:
            return
        plot.region = region
        region.add_plot(plot)
        for d in Direction:
            if self.in_bounds(x + d.x, y + d.y):
                self.fill_region(x + d.x, y + d.y, region)

    def get_fence_cost(self) -> int:
        if len(self.regions) == 0:
            self.fill_regions()
        return sum(r.get_fence_cost() for r in self.regions)

    def set_fence_lines(self) -> None:
        for region in self.regions:
            region.fence_lines = 0
        # TODO:  Replace
        for y in range(self.height):
            n_fence = s_fence = False
            cur_region = None
            for x in range(self.width):
                plot = self.plots[y][x]
                if cur_region != plot.region:
                    if not (plot.shares_region(plot.neighbors[Direction.N])):
                        n_fence = True
                        plot.region.fence_lines += 1
                    else:
                        n_fence = False
                    if not (plot.shares_region(plot.neighbors[Direction.S])):
                        s_fence = True
                        plot.region.fence_lines += 1
                    else:
                        s_fence = False
                    cur_region = plot.region
                else:
                    if n_fence and (plot.shares_region(plot.neighbors[Direction.N])):
                        n_fence = False
                    elif not (n_fence) and not (
                        plot.shares_region(plot.neighbors[Direction.N])
                    ):
                        n_fence = True
                        plot.region.fence_lines += 1
                    if s_fence and (plot.shares_region(plot.neighbors[Direction.S])):
                        s_fence = False
                    elif not (s_fence) and not (
                        plot.shares_region(plot.neighbors[Direction.S])
                    ):
                        s_fence = True
                        plot.region.fence_lines += 1

        for x in range(self.width):
            e_fence = w_fence = False
            cur_region = None
            for y in range(self.height):
                plot = self.plots[y][x]
                if cur_region != plot.region:
                    if not (plot.shares_region(plot.neighbors[Direction.W])):
                        w_fence = True
                        plot.region.fence_lines += 1
                    else:
                        w_fence = False
                    if not (plot.shares_region(plot.neighbors[Direction.E])):
                        e_fence = True
                        plot.region.fence_lines += 1
                    else:
                        e_fence = False
                    cur_region = plot.region
                else:
                    if w_fence and (plot.shares_region(plot.neighbors[Direction.W])):
                        w_fence = False
                    elif not (w_fence) and not (
                        plot.shares_region(plot.neighbors[Direction.W])
                    ):
                        w_fence = True
                        plot.region.fence_lines += 1
                    if e_fence and (plot.shares_region(plot.neighbors[Direction.E])):
                        e_fence = False
                    elif not (e_fence) and not (
                        plot.shares_region(plot.neighbors[Direction.E])
                    ):
                        e_fence = True
                        plot.region.fence_lines += 1

    def get_bulk_fence_cost(self) -> int:
        if len(self.regions) == 0:
            self.fill_regions()
        self.set_fence_lines()
        return sum(r.fence_lines * r.get_area() for r in self.regions)


def solution_one(data: List[List[int]]) -> int:
    field = Field(data)
    field.fill_regions()
    return field.get_fence_cost()


def solution_two(data: List[List[int]]) -> int:
    field = Field(data)
    field.fill_regions()
    return field.get_bulk_fence_cost()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("twelve", args.test)
    l = parse_data(dr)
    if args.one:
        print(solution_one(l))
    elif args.two:
        print(solution_two(l))
