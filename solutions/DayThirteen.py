import argparse
import math
import pathlib
import re
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


A_BUTTON_RE = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
B_BUTTON_RE = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
PRIZE_RE = re.compile(r"Prize: X=(\d+), Y=(\d+)")


def parse_data(
    data: Iterator[str],
) -> Iterator[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    a_button = b_button = prize_loc = None
    for line in data:
        if len(line.strip()) == 0:
            continue
        a_button = A_BUTTON_RE.match(line).groups()
        b_button = B_BUTTON_RE.match(next(data)).groups()
        prize_loc = PRIZE_RE.match(next(data)).groups()
        yield tuple(map(int, a_button)), tuple(map(int, b_button)), tuple(
            map(int, prize_loc)
        )


def get_best_cost_brute_force(
    a: Tuple[int, int], b: Tuple[int, int], test: Tuple[int, int]
) -> int:
    c = d = 0
    while c * a[0] < test[0]:
        c += 1
    best_cost = 0
    while c >= 0:
        if (c * a[0] + d * b[0]) == test[0]:
            if (c * a[1] + d * b[1]) == test[1]:
                # Alternatively, if not colinear this is unique
                best_cost = (3 * c + d) if best_cost == 0 else min(best_cost, 3 * c + d)
            c -= 1
        elif (c * a[0] + d * b[0]) > test[0]:
            c -= 1
        else:
            d += 1
    return best_cost


def get_best_cost(a: Tuple[int, int], b: Tuple[int, int], test: Tuple[int, int]) -> int:
    cost = (3, 1)
    if a[0] < b[0]:
        t = a
        a = b
        b = t
        cost = (1, 3)
    r0, r1 = a[0], b[0]
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while r1 > 0:
        q = math.copysign(abs(r0) // abs(r1), r1 * r0)
        r1, r0 = r0 - q * r1, r1
        s1, s0 = s0 - q * s1, s1
        t1, t0 = t0 - q * t1, t1
    start = test[0] // a[0]
    if (test[0] - start * a[0]) % r0 != 0:
        # Not a lattice point
        return 0
    # test[0] = start*a[0] + ((test[0] - start*a[0]) // r0) * (s0*a[0] + t0*b[0])
    # test[0] = (start + s0*((test[0] - start*a[0])//r0))* a[0] + t0*((test[0] - start*a[0])//r0) * b[0]
    f0 = start + s0 * ((test[0] - start * a[0]) // r0)
    f1 = t0 * ((test[0] - start * a[0]) // r0)
    if (s1 * a[1] + t1 * b[1]) == 0:
        if (f0 * a[1] + f1 * b[1]) != test[1]:
            return 0
        # In this case, the vectors are collinear
        # minimize cost[0]*(f0 + k*s1) + cost[1]*(f1 + k*t1) with (f0 + k*s1) > 0 and (f1 + k*t1) > 0
        if cost[0] > cost[1]:
            k = -(f0 // s1)
        else:
            k = -((-f1) // (-t1))
        return cost[0] * (f0 + k * s1) + cost[1] * (f1 + k * t1)
    if (test[1] - f0 * a[1] - f1 * b[1]) % (s1 * a[1] + t1 * b[1]) != 0:
        return 0
    adjust = (test[1] - f0 * a[1] - f1 * b[1]) // (s1 * a[1] + t1 * b[1])
    f0, f1 = f0 + adjust * s1, f1 + adjust * t1
    return cost[0] * f0 + cost[1] * f1


def solution_one(
    data: Iterator[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]
) -> int:
    return sum(get_best_cost(a, b, c) for a, b, c in data)


def solution_two(
    data: Iterator[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]
) -> int:
    return sum(
        get_best_cost(a, b, (c[0] + 10000000000000, c[1] + 10000000000000))
        for a, b, c in data
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("thirteen", args.test)
    l = parse_data(dr)
    if args.one:
        print(solution_one(l))
    elif args.two:
        print(solution_two(l))
