import sys
from itertools import product

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class Region:
    def __init__(self, idx: str, start_position: tuple[str, str]) -> None:
        self.positions = set([start_position])
        self.perimeter = 0
        self.idx = idx

    def price(self) -> int:
        return len(self.positions) * self.perimeter
    
    def __repr__(self) -> str:
        return f"Region {self.idx} in positions {self.positions}"


class Field:
    def __init__(self, field_map: list[str]) -> None:
        self.map = []
        self.regions = []
        self.field_map = field_map
        self.remaining = set(
            product(*[range(len(field_map)), range(len(field_map[0]))])
        )
        while self.remaining:
            self.fill_region()

    def fill_region(self):
        position = self.remaining.pop()
        queue = set([position])
        visited = set()
        idx = self.field_map[position[0]][position[1]]
        region = Region(idx, position)
        while queue:
            position = queue.pop()
            visited.add(position)
            for direction in DIRECTIONS:
                next_position = sum_duples(position, direction)
                if next_position in visited:
                    continue
                if self.out_of_bounds(next_position):
                    region.perimeter += 1
                    continue
                next_idx = self.field_map[next_position[0]][next_position[1]]
                if next_idx == idx:
                    queue.add(next_position)
                    region.positions.add(next_position)
                else:
                    region.perimeter += 1
        self.remaining.difference_update(region.positions)
        self.regions.append(region)

    def out_of_bounds(self, position: tuple[int, int]) -> bool:
        if 0 <= position[0] < len(self.field_map) and 0 <= position[1] < len(
            self.field_map[0]
        ):
            return False
        return True

    def price(self) -> int:
        return sum([region.price() for region in self.regions])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    field_map = open(file_name).read().strip().split("\n")
    field = Field(field_map)
    price = field.price()
    print(f"The total price of the field is {price}")
