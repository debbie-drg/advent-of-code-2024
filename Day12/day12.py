import sys
from itertools import product

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class Region:
    def __init__(self, idx: str, start_position: tuple[str, str]) -> None:
        self.positions = set([start_position])
        self.perimeter = 0
        self.corners = 0
        self.idx = idx

    def price(self) -> int:
        return len(self.positions) * self.perimeter

    def side_price(self) -> int:
        return len(self.positions) * self.corners

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
            region.corners += self.count_corners(position)
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

    def neighbourhood(self, position: tuple[int, int]) -> list[list[int]]:
        neighbourhood = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        idx = self.field_map[position[0]][position[1]]
        for row_index in range(3):
            for col_index in range(3):
                row_position = position[0] - 1 + row_index
                col_position = position[1] - 1 + col_index
                if self.out_of_bounds((row_position, col_position)):
                    continue
                next_idx = self.field_map[row_position][col_position]
                if next_idx == idx:
                    neighbourhood[row_index][col_index] = 1
        return neighbourhood

    def count_corners(self, position: tuple[int, int]) -> int:
        neighbourhood = self.neighbourhood(position)
        count = 0
        if neighbourhood[1][0] == 0 and neighbourhood[0][1] == 0:
            count += 1
        if (
            neighbourhood[0][0] == 0
            and neighbourhood[1][0] == 1
            and neighbourhood[0][1] == 1
        ):
            count += 1
        if neighbourhood[1][2] == 0 and neighbourhood[0][1] == 0:
            count += 1
        if (
            neighbourhood[0][2] == 0
            and neighbourhood[1][2] == 1
            and neighbourhood[0][1] == 1
        ):
            count += 1
        if neighbourhood[1][0] == 0 and neighbourhood[2][1] == 0:
            count += 1
        if (
            neighbourhood[2][0] == 0
            and neighbourhood[1][0] == 1
            and neighbourhood[2][1] == 1
        ):
            count += 1
        if neighbourhood[1][2] == 0 and neighbourhood[2][1] == 0:
            count += 1
        if (
            neighbourhood[2][2] == 0
            and neighbourhood[1][2] == 1
            and neighbourhood[2][1] == 1
        ):
            count += 1
        return count

    def out_of_bounds(self, position: tuple[int, int]) -> bool:
        if 0 <= position[0] < len(self.field_map) and 0 <= position[1] < len(
            self.field_map[0]
        ):
            return False
        return True

    def price(self) -> int:
        return sum([region.price() for region in self.regions])

    def bulk_price(self) -> int:
        return sum([region.side_price() for region in self.regions])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    field_map = open(file_name).read().strip().split("\n")
    field = Field(field_map)
    price = field.price()
    print(f"The total price of the field is {price}")
    bulk_price = field.bulk_price()
    print(f"With the bulk discount, the price is {bulk_price}")
