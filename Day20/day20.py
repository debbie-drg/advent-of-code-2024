import sys
import heapq
from collections import defaultdict
from functools import cache

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def manhattan_distance(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> int:
    return abs(duple_1[0] - duple_2[0]) + abs(duple_1[1] - duple_2[1])


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(duple: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(duple, direction) for direction in DIRECTIONS]


class RaceTrack:
    def __init__(self, race_map: str) -> None:
        self.walls = set()
        for row, line in enumerate(race_map.split("\n")):
            for col, char in enumerate(line):
                if char == "#":
                    self.walls.add((row, col))
                if char == "S":
                    self.start = (row, col)
                if char == "E":
                    self.end = (row, col)
        self.path = None

    def valid_neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        return [
            neighbour
            for neighbour in neighbours(position)
            if not neighbour in self.walls
        ]

    def shortest_path(self) -> list[tuple[int, int]]:
        queue = [(0, self.start)]
        path = []
        visited = set()
        while True:
            steps, position = heapq.heappop(queue)
            neighbours_to_check = self.valid_neighbours(position)
            for neighbour in neighbours_to_check:
                if neighbour in visited:
                    continue
                path.append(neighbour)
                visited.add(neighbour)
                if neighbour == self.end:
                    return path
                heapq.heappush(queue, (steps + 1, neighbour))

    def saved_over_100(self) -> tuple[int, int]:
        if self.path is None:
            self.path = self.shortest_path()
        cheats_count, cheats_count_20 = 0, 0
        for index, position in enumerate(self.path):
            difference = -1
            for other_position in self.path[index:]:
                difference += 1
                distance = manhattan_distance(position, other_position)
                if distance > 20:
                    continue
                steps_gained = difference - distance
                if steps_gained < 100:
                    continue
                cheats_count_20 += 1
                if distance <= 2:
                    cheats_count += 1
        return cheats_count, cheats_count_20


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    race_map = open(file_name).read().strip()
    race_track = RaceTrack(race_map)
    shortest_path = race_track.shortest_path()
    saved_by_cheating, saved_by_cheating_20 = race_track.saved_over_100()
    print(f"There are {saved_by_cheating} cheats saving over 100 picoseconds")
    print(f"Allowing cheats up to 20 steps, it's {saved_by_cheating_20}")
