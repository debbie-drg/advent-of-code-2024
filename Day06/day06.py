import sys

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class GuardMap:
    def __init__(self, world_map: str) -> None:
        self.obstacles = set()
        world_map_lines = world_map.split("\n")
        self.world_map_lines = world_map_lines
        for row_index, row in enumerate(world_map_lines):
            for col_index, char in enumerate(row):
                if char == "#":
                    self.obstacles.add((row_index, col_index))
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

    def creates_loop(self, added_obstacle) -> bool:
        if added_obstacle in self.create_loops:
            return True
        position = self.guard_start
        obstacles = self.obstacles | set([added_obstacle])
        direction = 0
        history = set([(0, position)])
        while not self.out_of_bounds(position):
            next_position = sum_duples(position, DIRECTIONS[direction])
            if next_position in obstacles:
                direction = (direction + 1) % 4
                continue
            if ((direction, next_position)) in history:
                return True
            position = next_position
            history.add((direction, position))
        return False

    def guard_run(self) -> int:
        while self.move_guard():
            pass
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
