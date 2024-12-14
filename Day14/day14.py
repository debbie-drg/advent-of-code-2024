import sys

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (1, 0)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def neighbours(position: tuple[int, int]) -> list[tuple[int, int]]:
    return [sum_duples(position, direction) for direction in DIRECTIONS]


class Robot:
    def __init__(self, robot_paramenters: str):
        pos, vel = robot_paramenters.split()
        pos = pos.split("=")[1].split(",")
        vel = vel.split("=")[1].split(",")
        self.start_pos = (int(pos[0]), int(pos[1]))
        self.vel = (int(vel[0]), int(vel[1]))

    def position(self, turn: int, height: int, width: int) -> tuple[int, int]:
        x_pos = (self.start_pos[0] + turn * self.vel[0]) % width
        y_pos = (self.start_pos[1] + turn * self.vel[1]) % height
        return (x_pos, y_pos)


class RobotField:
    def __init__(self, robots: str, height: int, width: int):
        self.robots = [Robot(parameters) for parameters in robots.split("\n")]
        self.height = height
        self.width = width

    def __repr__(self):
        return self.print_turn(0)

    def print_turn(self, turn: int):
        positions = [
            robot.position(turn, self.height, self.width) for robot in self.robots
        ]
        representation = ""
        for y_pos in range(self.height):
            current_line = ""
            for x_pos in range(self.width):
                count = positions.count((x_pos, y_pos))
                if count != 0:
                    representation += str(count)
                else:
                    representation += "."
            representation += current_line + "\n"
        return representation.strip()

    def quadrant(self, position: tuple[int, int]) -> int | None:
        if position[0] < self.width // 2:
            if position[1] < self.height // 2:
                return 0
            elif position[1] > self.height // 2:
                return 1
            else:
                return None
        elif position[0] > self.width // 2:
            if position[1] < self.height // 2:
                return 2
            elif position[1] > self.height // 2:
                return 3
            else:
                return None
        return None

    def safety_factor(self, turn: int) -> int:
        positions = [
            robot.position(turn, self.height, self.width) for robot in self.robots
        ]
        per_quadrant = [0, 0, 0, 0]
        for position in positions:
            try:
                per_quadrant[self.quadrant(position)] += 1
            except TypeError:
                continue
        return per_quadrant[0] * per_quadrant[1] * per_quadrant[2] * per_quadrant[3]

    def find_tree(self):
        index = 0
        while True:
            positions = [robot.position(index, self.height, self.width) for robot in self.robots]
            if len(positions) == len(set(positions)):
                return index
            index += 1

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    if "example" in file_name:
        height, width = 7, 11
    else:
        height, width = 103, 101
    input_data = open(file_name).read().strip()
    robot_field = RobotField(input_data, height, width)
    safety_factor = robot_field.safety_factor(100)
    print(f"After 100 seconds, the safety factor is {safety_factor}")
    if not "example" in file_name:
        tree_index = robot_field.find_tree()
        print(robot_field.print_turn(tree_index))
        print(f"Tree showed up at turn {tree_index}")
        print("Ho ho ho! Merry Christmas!")
