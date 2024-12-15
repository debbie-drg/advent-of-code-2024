import sys

DIRECTIONS = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class Box:
    def __init__(self, position: tuple[int, int], wide: bool = False) -> None:
        self.position = position
        self.wide = wide
        if wide:
            self.other_position = sum_duples(self.position, (0, 1))

    def __hash__(self) -> int:
        return self.position.__hash__()

    def in_box(self, position: tuple[int, int]) -> bool:
        if self.position == position:
            return True
        if self.wide:
            return position == self.other_position
        return False

    def update_position(self, movement: tuple[int, int]):
        self.position = sum_duples(movement, self.position)
        if self.wide:
            self.other_position = sum_duples(movement, self.other_position)

    def gps_coordinates(self):
        return 100 * self.position[0] + self.position[1]

    def get_positions(self) -> list[tuple[int, int]]:
        if not self.wide:
            return [self.position]
        return [self.position, self.other_position]

    def get_moved_positions(self, movement: tuple[int, int]) -> set[tuple[int, int]]:
        position_1 = sum_duples(self.position, movement)
        if not self.wide:
            return {position_1}
        position_2 = sum_duples(self.other_position, movement)
        return {position_1, position_2}


class Warehouse:
    def __init__(self, warehouse_map: str, wide: bool = False) -> None:
        split_map = warehouse_map.strip().split("\n")
        self.boxes = set()
        self.height = len(split_map)
        self.width = len(split_map[0])
        self.wide = wide
        if wide:
            self.width *= 2
        self.walls = set()
        for row_index, row in enumerate(split_map):
            for col_index, symbol in enumerate(row):
                if symbol == "O":
                    self.boxes.add(Box((row_index, (wide + 1) * col_index), wide))
                elif symbol == "@":
                    self.robot_position = (row_index, (wide + 1) * col_index)
                elif symbol == "#":
                    self.walls.add((row_index, (wide + 1) * col_index))
                    if wide:
                        self.walls.add((row_index, (wide + 1) * col_index + 1))

    def __repr__(self) -> str:
        repr_out = ""
        skip = False
        box_positions = set(box.position for box in self.boxes)
        for row in range(self.height):
            current_line = ""
            for col in range(self.width):
                if skip:
                    skip = False
                    continue
                if (row, col) in box_positions:
                    if self.wide:
                        current_line += "[]"
                        skip = True
                    else:
                        current_line += "O"
                elif (row, col) == self.robot_position:
                    current_line += "@"
                elif (row, col) in self.walls:
                    current_line += "#"
                else:
                    current_line += "."
            repr_out += current_line + "\n"
        return repr_out.strip()

    def in_box(self, position: tuple[int, int]) -> bool:
        for box in self.boxes:
            if box.in_box(position):
                return True
        return False

    def move_robot(self, command: str):
        direction = DIRECTIONS[command]
        next_position = sum_duples(self.robot_position, direction)
        if next_position in self.walls:
            return
        boxes_to_move = set()
        positions_to_check = {(next_position)}
        positions_checked = set()
        while positions_to_check:
            current_position = positions_to_check.pop()
            if current_position in self.walls:
                return
            for box in self.boxes:
                if box.in_box(current_position):
                    boxes_to_move.add(box)
                    box_next_positions = box.get_moved_positions(direction)
                    positions_to_check |= box_next_positions.difference(
                        positions_checked
                    )
                    positions_checked.add(current_position)
        if not boxes_to_move:
            self.robot_position = next_position
            return
        for box in boxes_to_move:
            box.update_position(direction)
        self.robot_position = sum_duples(self.robot_position, direction)

    def sum_of_coordinates(self) -> int:
        return sum(box.gps_coordinates() for box in self.boxes)

    def move_batch(self, instructions: str):
        for instruction in instructions:
            self.move_robot(instruction)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    warehouse_map, instructions = open(file_name).read().strip().split("\n\n")
    instructions = "".join(instructions.split("\n")).strip()
    warehouse = Warehouse(warehouse_map)
    warehouse.move_batch(instructions)
    print(f"The sum of GPS coordinates is {warehouse.sum_of_coordinates()}")
    wide_warehouse = Warehouse(warehouse_map, True)
    wide_warehouse.move_batch(instructions)
    print(f"With the new layout, it's {wide_warehouse.sum_of_coordinates()}")
