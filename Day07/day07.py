import sys

DECIMAL_REP = [int(float(f"1e{i}")) for i in range(16)]


def parse_data(input_data: str) -> list[tuple[int, list[int]]]:
    parsed_data = []
    lines = input_data.split("\n")
    for line in lines:
        goal, numbers = line.split(":")
        parsed_data.append((int(goal), [int(number) for number in numbers.split()]))
    return parsed_data


def concatenate(left_side: int, right_side: int) -> int:
    for element in DECIMAL_REP:
        if element > right_side:
            return left_side * element + right_side
    return 0


def is_valid(goal: int, result: int, remaining: list[int], concatenation: bool):
    if not remaining:
        return goal == result
    current = remaining[0]
    if is_valid(goal, result + current, remaining[1:], concatenation):
        return True
    if is_valid(goal, result * current, remaining[1:], concatenation):
        return True
    if concatenation and is_valid(
        goal, concatenate(result, current), remaining[1:], concatenation
    ):
        return True
    return False


def is_valid_equation(
    equation: tuple[int, list[int]], concatenation: bool = False
) -> bool:
    goal, numbers = equation
    return is_valid(goal, 0, numbers, concatenation)


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
