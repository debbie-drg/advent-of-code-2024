import sys
from collections import defaultdict


def mix(number: int, secret_number: int) -> int:
    return number ^ secret_number


def prune(number: int) -> int:
    return number % 16777216


def secret_number(number: int) -> int:
    mult = number << 6
    number = mix(mult, number)
    number = prune(number)
    div = number >> 5
    number = mix(div, number)
    number = prune(number)
    mult = number << 11
    number = mix(mult, number)
    return prune(number)


def iterate_secret_number(
    number: int, times: int
) -> tuple[int, defaultdict[tuple[int], int]]:
    banana_counts = defaultdict(int)
    sequence = (None, None, None, None)
    for index in range(times):
        last_price = number % 10
        number = secret_number(number)
        new_price = number % 10
        change = new_price - last_price
        sequence = (*sequence[1:], change)
        if index >= 3 and sequence not in banana_counts:
            banana_counts[sequence] = new_price
    return number, banana_counts


def mix_dicts(
    dict_1: defaultdict[tuple[int], int], dict_2: defaultdict[tuple[int], int]
) -> defaultdict[tuple[int], int]:
    for key in dict_2:
        dict_1[key] += dict_2[key]
    return dict_1


def sum_and_best_price(buyer_numbers: list[int]) -> tuple[int, int]:
    banana_counts = defaultdict(int)
    secret_sum = 0
    for number in buyer_numbers:
        secret, banana_count = iterate_secret_number(number, 2000)
        secret_sum += secret
        banana_counts = mix_dicts(banana_counts, banana_count)
    return secret_sum, max(banana_counts.values())


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    buyer_numbers = [
        int(number) for number in open(file_name).read().strip().split("\n")
    ]
    secret_sum, max_bananas = sum_and_best_price(buyer_numbers)
    print(f"The sum of the secret numbers is {secret_sum}")
    print(f"The maximum number of banans you can get is {max_bananas}")
