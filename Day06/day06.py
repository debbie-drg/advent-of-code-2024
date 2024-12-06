import sys
from copy import deepcopy

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class GuardMap:
    def __init__(self, world_map: str) -> None:
        self.obstacles = set()
        world_map_lines = world_map.split("\n")
        self.world_map_lines = world_map_lines
        self.per_row_obstacles = [[] for _ in range(len(self.world_map_lines))]
        self.per_col_obstacles = [[] for _ in range(len(self.world_map_lines[0]))]
        for row_index, row in enumerate(world_map_lines):
            for col_index, char in enumerate(row):
                if char == "#":
                    self.obstacles.add((row_index, col_index))
                    self.per_row_obstacles[row_index].append(col_index)
                    self.per_col_obstacles[col_index].append(row_index)
                if char == "^":
                    self.guard_position = (row_index, col_index)
        self.guard_direction = 0
        self.guard_start = self.guard_position
        self.visited = set([self.guard_position])
        self.history = set([(0, self.guard_position)])
        self.upper_bounds = [len(world_map_lines), len(world_map_lines[0])]
        self.create_loops = set()

    def out_of_bounds(self, position: tuple[int, int]) -> bool:
        if position[0] < 0 or position[1] < 0:
            return True
        if position[0] >= self.upper_bounds[0] or position[1] >= self.upper_bounds[1]:
            return True
        return False

    def move_guard(self) -> bool:
        next_position = sum_duples(
            self.guard_position, DIRECTIONS[self.guard_direction]
        )
        if next_position in self.obstacles:
            self.guard_direction += 1
            self.guard_direction %= 4
            return self.move_guard()
        elif self.out_of_bounds(next_position):
            return False
        else:
            if self.creates_loop(next_position):
                self.create_loops.add(next_position)
        self.visited.add(next_position)
        self.history.add((self.guard_direction, self.guard_position))
        self.guard_position = next_position
        return True

    @staticmethod
    def position_before_next_obstacle(
        position: tuple[int, int],
        direction: int,
        per_row_obstacles: list[list[int]],
        per_col_obstacles: list[list[int]],
    ) -> tuple[int, int] | None:
        if direction in [0, 2]:
            col = position[1]
            if direction == 0:
                values = [
                    value for value in per_col_obstacles[col] if value < position[0]
                ]
                if not values:
                    return None
                return (max(values) + 1, col)
            else:
                values = [
                    value for value in per_col_obstacles[col] if value > position[0]
                ]
                if not values:
                    return None
                return (min(values) - 1, col)
        else:
            row = position[0]
            if direction == 1:
                values = [
                    value for value in per_row_obstacles[row] if value > position[1]
                ]
                if not values:
                    return None
                return (row, min(values) - 1)
            else:
                values = [
                    value for value in per_row_obstacles[row] if value < position[1]
                ]
                if not values:
                    return None
                return (row, max(values) + 1)

    def creates_loop(self, added_obstacle: tuple[int, int]) -> bool:
        if added_obstacle in self.create_loops:
            return True
        per_row_obstacles = deepcopy(self.per_row_obstacles)
        per_col_obstacles = deepcopy(self.per_col_obstacles)
        per_row_obstacles[added_obstacle[0]].append(added_obstacle[1])
        per_col_obstacles[added_obstacle[1]].append(added_obstacle[0])
        position = self.guard_start
        direction = 0
        history = set([(0, position)])
        while True:
            next_position = self.position_before_next_obstacle(
                position, direction, per_row_obstacles, per_col_obstacles
            )
            if next_position is None:
                return False
            if ((direction, next_position)) in history:
                return True
            position = next_position
            history.add((direction, position))
            direction = (direction + 1) % 4

    def guard_run(self) -> int:
        while self.move_guard():
            pass
        self.create_loops.remove((sum_duples(self.guard_start, DIRECTIONS[0])))
        return len(self.visited)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    guard_map = GuardMap(input_data)
    visited = guard_map.guard_run()
    print(f"The guard visited {visited} positions")
    print(
        f"There are {len(guard_map.create_loops)} possible spots to place an obstacle and create a loop"
    )
