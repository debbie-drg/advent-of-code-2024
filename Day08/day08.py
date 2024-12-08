import sys
from collections import defaultdict
from itertools import combinations


def duple_difference(
    duple_1: tuple[int, int], duple_2: tuple[int, int]
) -> tuple[int, int]:
    return (duple_2[0] - duple_1[0], duple_2[1] - duple_1[1])


def duple_sum(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class AntenaField:
    def __init__(self, map: list[str]) -> None:
        self.antennas = defaultdict(set)
        for row_index, row in enumerate(map):
            for col_index, char in enumerate(row):
                if char != ".":
                    self.antennas[char].add((row_index, col_index))
        self.length = len(map[0])
        self.depth = len(map)

    def in_grid(self, position: tuple[int, int]) -> bool:
        return (0 <= position[0] < self.depth) and (0 <= position[1] < self.length)

    def antinodes(
        self,
        antenna_1: tuple[int, int],
        antenna_2: tuple[int, int],
        respect_distances: bool = True,
    ) -> set[tuple[int, int]]:
        antinode_set = set()
        if not respect_distances:
            antinode_set.add(antenna_1)
            antinode_set.add(antenna_2)
        difference = duple_difference(antenna_1, antenna_2)
        next_position = antenna_2
        while True:
            next_position = duple_sum(next_position, difference)
            if self.in_grid(next_position):
                antinode_set.add(next_position)
            else:
                break
            if respect_distances:
                break
        difference = duple_difference(antenna_2, antenna_1)
        next_position = antenna_1
        while True:
            next_position = duple_sum(difference, next_position)
            if self.in_grid(next_position):
                antinode_set.add(next_position)
            else:
                break
            if respect_distances:
                break
        return antinode_set

    def antinodes_per_class(self, antenna_class: str, respect_distances: bool = True):
        antinode_set = set()
        for antenna_1, antenna_2 in combinations(self.antennas[antenna_class], 2):
            antinode_set.update(self.antinodes(antenna_1, antenna_2, respect_distances))
        return antinode_set

    def all_antinodes(self, respect_distances: bool = True):
        antinode_set = set()
        for antenna_class in self.antennas:
            antinode_set.update(
                self.antinodes_per_class(antenna_class, respect_distances)
            )
        return antinode_set


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split()
    antena_field = AntenaField(input_data)
    print(f"There are {len(antena_field.all_antinodes())} antinodes.")
    print(f"If distances don't matter, it's {len(antena_field.all_antinodes(False))}.")
