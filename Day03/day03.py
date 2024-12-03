import sys
import re

MATCH_MULS = r"mul\([0-9]+,[0-9]+\)"


def find_all_muls(input_data: str) -> list[str]:
    return re.findall(MATCH_MULS, input_data)


def do_mul(mul: str) -> int:
    number_1, number_2 = [int(element) for element in re.findall("[0-9]+", mul)]
    return number_1 * number_2


def with_do_dont(input_data: str):
    input_data = "ISTART" + input_data.replace("don't()", "IEND").replace(
        "do()", "ISTART"
    )
    sections = input_data.split("I")
    muls = [
        find_all_muls(section) for section in sections if section.startswith("START")
    ]
    return sum(sum(do_mul(mul) for mul in inner_mul) for inner_mul in muls)


def add_all_muls(input_data: str) -> int:
    return sum([do_mul(mul) for mul in find_all_muls(input_data)])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    print(f"The sum of all multiplications is {add_all_muls(input_data)}")
    print(f"Observing the do/don't instructions, it's {with_do_dont(input_data)}")
