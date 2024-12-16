import sys
import heapq

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


class ReindeerMaze:
    def __init__(self, maze_map: str) -> None:
        maze_lines = maze_map.split()
        self.walls = set()
        self.depth = len(maze_lines)
        self.width = len(maze_lines[0])
        for row_index, line in enumerate(maze_lines):
            for col_index, char in enumerate(line):
                if char == "#":
                    self.walls.add((row_index, col_index))
                if char == "S":
                    self.start = (row_index, col_index)
                if char == "E":
                    self.end = (row_index, col_index)

    def __repr__(self) -> str:
        maze = ""
        for row_index in range(self.depth):
            maze_line = ""
            for col_index in range(self.width):
                if (row_index, col_index) in self.walls:
                    maze_line += "#"
                elif (row_index, col_index) == self.start:
                    maze_line += "S"
                elif (row_index, col_index) == self.end:
                    maze_line += "E"
                else:
                    maze_line += "."
            maze_line += "\n"
            maze += maze_line
        return maze.strip()

    def print_path(self, path) -> str:
        maze = ""
        for row_index in range(self.depth):
            maze_line = ""
            for col_index in range(self.width):
                if (row_index, col_index) in self.walls:
                    maze_line += "#"
                elif (row_index, col_index) == self.start:
                    maze_line += "S"
                elif (row_index, col_index) == self.end:
                    maze_line += "E"
                elif (row_index, col_index) in path:
                    maze_line += "p"
                else:
                    maze_line += "."
            maze_line += "\n"
            maze += maze_line
        return maze.strip()

    def valid_neighbours(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        possible_neighbours = [
            sum_duples(position, direction) for direction in DIRECTIONS
        ]
        return [
            neighbour
            for neighbour in possible_neighbours
            if neighbour not in self.walls
        ]

    def valid_directions(self, position: tuple[int, int]) -> list[int]:
        directions = []
        for index, direction in enumerate(DIRECTIONS):
            if sum_duples(position, direction) not in self.walls:
                directions.append(index)
        return directions

    def cheapest_path(self) -> tuple[int, int]:
        queue = [(0, 0, self.start, set([self.start]))]
        best_score = None
        best_scores = {(self.start, 0): 0}
        end_path_tiles = set([self.end])
        while True:
            score, direction, position, path_tiles = heapq.heappop(queue)
            if best_score is not None:
                if score > best_score:
                    return best_score, len(end_path_tiles)
            next_position = sum_duples(position, DIRECTIONS[direction])
            if next_position not in self.walls:
                if next_position == self.end:
                    if best_score is None:
                        best_score = score + 1
                        end_path_tiles = path_tiles.union([self.end])
                    elif best_score < score + 1:
                        continue
                    elif best_score == score + 1:
                        end_path_tiles |= path_tiles
                    else:
                        best_score = score + 1
                        end_path_tiles = path_tiles.union([self.end])
                    continue
                if (next_position, direction) in best_scores:
                    if best_scores[(next_position, direction)] < score:
                        continue
                best_scores[(next_position, direction)] = score
                heapq.heappush(
                    queue,
                    (
                        score + 1,
                        direction,
                        next_position,
                        path_tiles.union([next_position]),
                    ),
                )
            possible_directions = self.valid_directions(position)
            for possible_direction in possible_directions:
                if possible_direction == direction:
                    continue
                direction_difference = (direction - possible_direction) % 4
                new_score = score + [0, 1000, 2000, 1000][direction_difference]
                if (position, possible_direction) in best_scores:
                    if best_scores[(position, possible_direction)] < new_score:
                        continue
                best_scores[(position, possible_direction)] = new_score
                heapq.heappush(
                    queue,
                    (
                        new_score,
                        possible_direction,
                        position,
                        path_tiles,
                    ),
                )


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    reindeer_maze = ReindeerMaze(input_data)
    cheapest_path, tiles_in_path = reindeer_maze.cheapest_path()
    print(f"The best path score is {cheapest_path}")
    print(f"The number of tiles in best score paths is {tiles_in_path}")
