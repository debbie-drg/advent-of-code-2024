import sys
import heapq
import re

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(duple: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(duple, direction) for direction in DIRECTIONS]


def parse_corrupted(data: str) -> tuple[int, int]:
    digits = re.findall("[0-9]+", data)
    return (int(digits[0]), int(digits[1]))


class MemoryArray:
    def __init__(self, corrupted: list[str], size: int) -> None:
        self.corrupted = set()
        self.size = size
        for line in corrupted:
            self.corrupted.add(parse_corrupted(line))

    def in_bounds(self, position: tuple[int, int]) -> bool:
        return 0 <= position[0] <= self.size and 0 <= position[1] <= self.size

    def shortest_path(self) -> tuple[int, set[tuple[int, int]]] | tuple[None, None]:
        queue = [(0, (0, 0), set([(0, 0)]))]
        visited = set([(0, 0)])
        while queue:
            steps, position, path = heapq.heappop(queue)
            neighbours_to_check = neighbours(position)
            for neighbour in neighbours_to_check:
                if not self.in_bounds(neighbour):
                    continue
                if neighbour in self.corrupted:
                    continue
                if neighbour in visited:
                    continue
                if neighbour == (self.size, self.size):
                    return steps + 1, path | set([neighbour])
                visited.add(neighbour)
                heapq.heappush(queue, (steps + 1, neighbour, path | set([neighbour])))
        return None, None

    def first_byte_blocking(self, corrupted: list[str]) -> tuple[int, int] | None:
        _, shortest_path = self.shortest_path()
        if shortest_path is None:
            return None
        for element in corrupted:
            parsed_element = parse_corrupted(element)
            self.corrupted.add(parsed_element)
            if parsed_element not in shortest_path:
                continue
            _, shortest_path = self.shortest_path()
            if shortest_path is None:
                return parsed_element


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    corrupted_blocks = open(file_name).read().strip().split("\n")
    size = 6 if "example" in file_name else 70
    fallen = 12 if "example" in file_name else 1024
    memory_array = MemoryArray(corrupted_blocks[:fallen], size)
    shortest_path_length, _ = memory_array.shortest_path()
    print(f"The length of the shortest path is {shortest_path_length}")
    first_byte = memory_array.first_byte_blocking(corrupted_blocks[fallen:])
    print(f"The first byte blocking the exit is {first_byte}")
