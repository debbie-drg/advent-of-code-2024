from functools import cache
import sys
from itertools import permutations

POSITIONS = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
    "^": (0, 1),
    "a": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

DIRECTIONS = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
}

INVERSE_DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def duple_difference(
    duple_1: tuple[int, int], duple_2: tuple[int, int]
) -> tuple[int, int]:
    return (duple_2[0] - duple_1[0], duple_2[1] - duple_1[1])


def passes_position(
    moves_string: str, start: tuple[int, int], avoid: tuple[int, int]
) -> bool:
    position = start
    for char in moves_string:
        position = sum_duples(position, INVERSE_DIRECTIONS[char])
        if position == avoid:
            return True
    return False


def generate_path(
    start: tuple[int, int], end: tuple[int, int], avoid: tuple[int, int]
) -> set[str]:
    diff_x, diff_y = duple_difference(start, end)
    dir_x = "" if diff_x == 0 else DIRECTIONS[(diff_x // abs(diff_x), 0)]
    dir_y = "" if diff_y == 0 else DIRECTIONS[(0, diff_y // abs(diff_y))]
    moves_string = dir_x * abs(diff_x) + dir_y * abs(diff_y)
    possible_strings = [
        ("".join(string) + "a")
        for string in permutations(moves_string)
        if not passes_position("".join(string), start, avoid)
    ]
    if not possible_strings:
        return {"a"}
    return set(possible_strings)


@cache
def shortest_length(code: str, num_robots: int = 2, current_robot: int = 0) -> int:
    current_position = (3, 2) if current_robot == 0 else (0, 2)
    avoid = (3, 0) if current_robot == 0 else (0, 0)

    number_moves = 0

    for character in code:
        next_position = POSITIONS[character]
        possible_moves = generate_path(current_position, next_position, avoid)
        if num_robots == current_robot:
            number_moves += len(possible_moves.pop())
        else:
            number_moves += min(
                shortest_length(move, num_robots, current_robot + 1)
                for move in possible_moves
            )
        current_position = next_position

    return number_moves


def complexity(code: str, num_robots: int = 2):
    return shortest_length(code, num_robots) * int(code[:-1])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    codes = open(file_name).read().strip().split("\n")
    total_complexity = sum(map(complexity, codes))
    print(f"The sum of the complexities is {total_complexity}")
    total_complexity = sum(map(lambda code: complexity(code, 25), codes))
    print(f"With the additional robots, it's {total_complexity}")
