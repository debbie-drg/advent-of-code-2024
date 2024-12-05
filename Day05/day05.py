import sys
from collections import defaultdict


def parse_pages(input_data: str) -> tuple[list[list[int]], list[list[int]]]:
    instructions, pages = input_data.split("\n\n")
    instructions = [
        [int(page) for page in group.split("|")]
        for group in instructions.strip().split("\n")
    ]
    pages = [
        [int(page) for page in group.split(",")] for group in pages.strip().split("\n")
    ]
    return instructions, pages


def next_pages_dict(instructions: list[list[int]]) -> dict[int, set[int]]:
    next_pages = defaultdict(set)
    for instruction in instructions:
        next_pages[instruction[0]].add(instruction[1])
    return next_pages


def in_order(next_pages: dict[int, set[int]], page_list: list[int]) -> bool:
    for index, page in enumerate(page_list):
        for previous in page_list[:index]:
            if previous in next_pages[page]:
                return False
    return True


def middle_element(page_list: list[int]) -> int:
    return page_list[len(page_list) // 2]


def add_middle_pages(instructions: list[list[int]], pages: list[list[int]]):
    next_pages = next_pages_dict(instructions)
    return sum([in_order(next_pages, page) * middle_element(page) for page in pages])


def order_pages(next_pages: dict[int, set[int]], pages: list[int]) -> list[int]:
    ordered_page = []
    while pages:
        page = pages.pop(0)
        for remaining in pages:
            if not remaining in next_pages[page]:
                pages.append(page)
                break
        else:
            ordered_page.append(page)
    return ordered_page


def order_and_middle(next_pages: dict[int, set[int]], pages: list[int]) -> int:
    if in_order(next_pages, pages):
        return 0
    return middle_element(order_pages(next_pages, pages))


def order_and_sum_middles(
    instructions: list[list[int]], pages_list: list[list[int]]
) -> int:
    next_pages = next_pages_dict(instructions)
    return sum([order_and_middle(next_pages, pages) for pages in pages_list])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    instructions, pages = parse_pages(input_data)
    print(
        f"The sum of the middle pages for the valid lists is {add_middle_pages(instructions, pages)}."
    )
    print(
        f"For the now ordered out of order lists, the sum is {order_and_sum_middles(instructions, pages)}."
    )
