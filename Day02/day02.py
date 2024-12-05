import sys


def parse_table(input_data: list[str]) -> list[list[int]]:
    parsed_data = []
    for line in input_data:
        parsed_data.append([int(number) for number in line.split()])
    return parsed_data


def is_safe(data: list[int], can_remove_one: bool) -> bool:
    if can_remove_one:
        for index in range(len(data)):
            if is_safe(data[:index] + data[index + 1 :], False):
                return True
        return False
    if len(data) > len(set(data)):
        return False
    ascending = sorted(data)
    if data != ascending and data != ascending[::-1]:
        return False
    return (
        max([abs(data[index] - data[index + 1]) for index in range(len(data) - 1)]) < 4
    )


def count_safe(parsed_data: list[list[int]], can_remove_one: bool = False) -> int:
    return sum(map(lambda data: is_safe(data, can_remove_one), parsed_data))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split("\n")
    parsed_data = parse_table(input_data)
    print(f"There are {count_safe(parsed_data)} safe reports.")
    print(f"Allowing to remove one, there are {count_safe(parsed_data, True)}.")
