import sys

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def map_position(topo_map: list[str], position: tuple[int, int]) -> int | None:
    if 0 <= position[0] < len(topo_map) and 0 <= position[1] < len(topo_map[0]):
        return int(topo_map[position[0]][position[1]])
    return None


def score_per_trailhead(
    topo_map: list[str], position: tuple[int, int]
) -> tuple[int, int]:
    current_value = 0
    paths = [[position]]
    while current_value < 9:
        next_paths = []
        while paths:
            path = paths.pop()
            last_position = path[-1]
            for direction in DIRECTIONS:
                next_position = sum_duples(direction, last_position)
                next_value = map_position(topo_map, next_position)
                if next_value == current_value + 1:
                    next_paths.append(path + [next_position])
        current_value += 1
        paths = next_paths
    tailheads = set([path[-1] for path in paths])
    return len(tailheads), len(paths)


def map_score(topo_map: list[str]) -> tuple[int, int]:
    score_tailheads, score_paths = 0, 0
    for row_index, row in enumerate(topo_map):
        for col_index in range(len(row)):
            if topo_map[row_index][col_index] == "0":
                current_tails, current_paths = score_per_trailhead(
                    topo_map, (row_index, col_index)
                )
                score_tailheads += current_tails
                score_paths += current_paths
    return score_tailheads, score_paths


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    topo_map = open(file_name).read().strip().split()
    score_tailheads, score_paths = map_score(topo_map)
    print(
        f"The sum of scores is {score_tailheads} for tailheads and {score_paths} for paths"
    )
