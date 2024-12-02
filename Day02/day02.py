import sys
from collections import defaultdict


def parse_table(input_data: list[str]) -> tuple[list[int], list[int]]:
    parsed_data = []
    for line in input_data:
        parsed_data.append([int(number) for number in line.split()])
    return parsed_data


def count_safe(parsed_data: list[list[int]]) -> int:
    safe = 0
    for line in parsed_data:
        sorted_line = sorted(line)
        reverse_sorted_line = sorted(line, reverse=True)
        if (sorted_line != line) and (reverse_sorted_line != line):
            continue
        count = True
        for index in range(len(line) - 1):
            if abs(line[index] - line[index + 1]) > 3:
                count = False
                break
            if line[index] == line[index + 1]:
                count = False
                break
        if not count:
            continue
        safe += 1
    return safe


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split("\n")
    parsed_data = parse_table(input_data)
    print(f"There are {count_safe(parsed_data)} safe reports.")
