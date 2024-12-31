import sys
from collections import defaultdict
from multiprocessing import Pool

PRUNE = 0xFFFFFF


def secret_number(number: int) -> int:
    number = ((number << 6) ^ number) & PRUNE
    number = ((number >> 5) ^ number) & PRUNE
    return ((number << 11) ^ number) & PRUNE


def iterate_secret_number(number: int) -> tuple[int, defaultdict[tuple[int], int]]:
    banana_counts = defaultdict(int)
    sequence = (None, None, None, None)
    for index in range(2000):
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
    pool = Pool()
    results = list(pool.imap_unordered(iterate_secret_number, buyer_numbers))
    for secret, banana_count in results:
        secret_sum += secret
        banana_counts = mix_dicts(banana_counts, banana_count)
    pool.close()
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
