import sys
from collections import defaultdict


class StoneLine:
    def __init__(self, stones: str) -> None:
        stone_list = [int(element) for element in stones.split()]
        stone_set = set(stone_list)
        self.stones = {stone: stone_list.count(stone) for stone in stone_set}

    def __repr__(self) -> str:
        return "Stone line: " + str(self.stones)

    def blink(self):
        new_stones = defaultdict(int)
        for stone in self.stones:
            number_stones = self.stones[stone]
            if stone == 0:
                new_stones[1] += number_stones
            elif len(str(stone)) % 2 == 0:
                str_rep = str(stone)
                stone_1 = int(str_rep[: len(str_rep) // 2])
                stone_2 = int(str_rep[len(str_rep) // 2 :])
                new_stones[stone_1] += number_stones
                new_stones[stone_2] += number_stones
            else:
                new_stones[2024 * stone] += number_stones
        self.stones = new_stones

    def blink_25_75(self) -> tuple[int, int]:
        blinks_25, blinks_75 = 0, 0
        for number_blinks in range(76):
            if number_blinks == 25:
                blinks_25 = sum(self.stones.values())
            if number_blinks == 75:
                blinks_75 = sum(self.stones.values())
            self.blink()
        return blinks_25, blinks_75


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    stones = open(file_name).read().strip()
    stone_line = StoneLine(stones)
    blink_25, blink_75 = stone_line.blink_25_75()
    print(f"The number of stones after 25 blinks is {blink_25}")
    print(f"After 75 blinks, it's {blink_75}")
