import sys
import re


def cramer_solve(matrix: list[list[int]], values: list[int]) -> list[int] | None:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant == 0:
        return None
    deti1 = values[0] * matrix[1][1] - values[1] * matrix[0][1]
    if deti1 % determinant != 0:
        return None
    deti1 //= determinant
    deti2 = matrix[0][0] * values[1] - matrix[1][0] * values[0]
    if deti2 % determinant != 0:
        return None
    deti2 //= determinant
    return [deti1, deti2]


def parse_and_solve(
    equation: str, corrected_coordinates: bool = False
) -> list[int]:
    split_equation = equation.split("\n")
    matrix_1 = re.findall("[0-9]+", split_equation[0])
    matrix_2 = re.findall("[0-9]+", split_equation[1])
    matrix = [
        [int(matrix_1[0]), int(matrix_2[0])],
        [int(matrix_1[1]), int(matrix_2[1])],
    ]
    values = [int(element) for element in re.findall("[0-9]+", split_equation[2])]
    if corrected_coordinates:
        values[0] += 10000000000000
        values[1] += 10000000000000
    solution = cramer_solve(matrix, values)
    if solution is None:
        return [0, 0]
    return [solution[0] * 3, solution[1]]


def minimum_tokens(input: str, corrected_coordinates: bool = False):
    return sum(
        [
            sum(parse_and_solve(equation, corrected_coordinates))
            for equation in input.split("\n\n")
        ]
    )


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    print(
        f"The minimum tokens to spend to win all possible prices is {minimum_tokens(input_data)}"
    )
    print(f"With the corrected coordinates, it's {minimum_tokens(input_data, True)}")
