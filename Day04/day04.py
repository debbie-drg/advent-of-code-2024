import sys


def transpose(input_data: list[str]) -> list[str]:
    return [
        "".join([input_data[i][j] for i in range(len(input_data))])
        for j in range(len(input_data[0]))
    ]


def diagonals(input_data: list[str]) -> list[str]:
    part_1 = [
        "".join([input_data[i - j][j] for j in range(i + 1)])
        for i in range(len(input_data))
    ]
    part_2 = [
        "".join(
            [
                input_data[len(input_data) - 1 - j][i + j]
                for j in range(len(input_data) - i)
            ]
        )
        for i in range(1, len(input_data))
    ]
    return part_1 + part_2


def count_xmas(input_data: list[str]) -> int:
    count = 0
    transposed = transpose(input_data)
    diagonals_1 = diagonals(input_data)
    diagonals_2 = diagonals(input_data[::-1])
    for array in [input_data, transposed, diagonals_1, diagonals_2]:
        for line in array:
            count += line.count("XMAS") + line.count("SAMX")
    return count


def count_x_mas(input_data: list[str]) -> int:
    count = 0
    for row in range(1, len(input_data) - 1):
        for col in range(1, len(input_data) - 1):
            if input_data[row][col] != "A":
                continue
            check_str = "".join(
                [
                    input_data[i][j]
                    for (i, j) in [
                        (row + 1, col - 1),
                        (row + 1, col + 1),
                        (row - 1, col - 1),
                        (row - 1, col + 1),
                    ]
                ]
            )
            if check_str in ["MMSS", "MSMS", "SMSM", "SSMM"]:
                count += 1
    return count


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip().split("\n")
    print(f"The word XMAS appears {count_xmas(input_data)} times.")
    print(f"There are {count_x_mas(input_data)} X-MAX.")
