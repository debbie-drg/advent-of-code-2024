import sys
import functools


def parse_towels(towels: str):
    global TOWELS
    TOWELS = sorted(
        [towel.strip() for towel in towels.split(",")], key=len, reverse=True
    )


@functools.cache
def is_possible(towel_pattern: str, count: int = 0) -> int:
    if len(towel_pattern) == 0:
        return 1
    for towel in TOWELS:
        if towel_pattern[: len(towel)] == towel:
            count += is_possible(towel_pattern[len(towel) :])
    return count


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    towels, combinations = open(file_name).read().strip().split("\n\n")
    parse_towels(towels)
    possible_patterns = list(map(is_possible, combinations.split("\n")))
    print(
        f"Of the patterns, {sum([True for element in possible_patterns if element != 0])} are possible"
    )
    print(f"There are {sum(possible_patterns)} ways to arrange them")
