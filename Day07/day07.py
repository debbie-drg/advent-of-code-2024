import sys
from itertools import product


def parse_data(input_data: str) -> list[tuple[int, list[int]]]:
    parsed_data = []
    lines = input_data.split("\n")
    for line in lines:
        goal, numbers = line.split(":")
        parsed_data.append((int(goal), [int(number) for number in numbers.split()]))
    return parsed_data


def is_valid_equation(
    equation: tuple[int, list[int]], concatenation: bool = False
) -> bool:
    goal, numbers = equation
    number_operations = 3 if concatenation else 2
    for operation_list in product(
        *[range(number_operations) for _ in range(len(numbers) - 1)]
    ):
        result = numbers[0]
        for index, operation in enumerate(operation_list):
            if operation == 0:
                result += numbers[index + 1]
            elif operation == 1:
                result *= numbers[index + 1]
            else:
                result = int(str(result) + str(numbers[index + 1]))
            if result > goal:
                break
        if result == goal:
            return True
    return False


def sum_valid(equations: list[tuple[int, list[int]]]) -> tuple[int, int]:
    remaining = []
    valid_sum = 0
    for equation in equations:
        if is_valid_equation(equation):
            valid_sum += equation[0]
        else:
            remaining.append(equation)
    with_concatenation = sum(
        [equation[0] for equation in remaining if is_valid_equation(equation, True)]
    )
    return valid_sum, valid_sum + with_concatenation


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    parsed_data = parse_data(input_data)
    valid, valid_with_concatenation = sum_valid(parsed_data)
    print(f"The sum of valid equations is {valid}.")
    print(f"Allowing concatenation, it's {valid_with_concatenation}.")
