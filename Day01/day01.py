import sys
from collections import defaultdict


def parse_columns(input_data: list[str]) -> tuple[list[int], list[int]]:
    left_list, right_list = [], []
    for line in input_data:
        num_1, num_2 = (int(number) for number in line.split())
        left_list.append(num_1)
        right_list.append(num_2)
    return left_list, right_list


def list_distance(left_list: list[int], right_list: list[int]) -> int:
    sorted_left = sorted(left_list)
    sorted_right = sorted(right_list)
    result = 0
    result = sum(
        [
            abs(sorted_right[index] - sorted_left[index])
            for index in range(len(sorted_left))
        ]
    )
    return result


def similarity_score(left_list: list[int], right_list: list[int]) -> int:
    right_list_counts = defaultdict(int)
    for element in right_list:
        right_list_counts[element] += 1
    return sum([element * right_list_counts[element] for element in left_list])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split("\n")
    left_list, right_list = parse_columns(input_data)
    print(f"The list difference is {list_distance(left_list, right_list)}")
    print(f"The similarity score is {similarity_score(left_list, right_list)}")
