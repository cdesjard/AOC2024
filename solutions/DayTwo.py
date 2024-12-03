import argparse
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


def parse_data(data_reader: Iterator[str]) -> Iterator[Iterator[int]]:
    return (map(int, line.split()) for line in data_reader)


def check_list(report: list[int], allowed_errors: int = 0) -> bool:
    # Check if decreasing in between steps of 1 and 3
    if allowed_errors < 0:
        return False
    for n in range(len(report) - 1):
        if not (1 <= report[n] - report[n + 1] <= 3):
            return check_list(
                report[n - 1 : n] + report[n + 1 :], allowed_errors - 1
            ) or check_list(report[n : n + 1] + report[n + 2 :], allowed_errors - 1)
    return True


def part_one(reports: Iterator[Iterator[int]]) -> int:
    safe_count = 0
    for report in reports:
        report_l = list(report)
        safe_count += check_list(report_l) or check_list(report_l[::-1])
    return safe_count


def part_two(reports: Iterator[Iterator[int]]) -> int:
    safe_count = 0
    for report in reports:
        report_l = list(report)
        safe_count += check_list(report_l, 1) or check_list(report_l[::-1], 1)
    return safe_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--one", action="store_true")
    group.add_argument("--two", action="store_true")
    args = parser.parse_args()
    dr = data_reader("two", args.test)
    l = parse_data(dr)
    if args.one:
        print(part_one(l))
    elif args.two:
        print(part_two(l))
