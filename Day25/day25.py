import sys


class KeysAndLocks:
    def __init__(self, input_data: str) -> None:
        self.keys = []
        self.locks = []
        split_input = input_data.split("\n\n")
        for element in split_input:
            if element[0] == "#":
                self.locks.append(self.parse(element, True))
            else:
                self.keys.append(self.parse(element, False))

    def parse(self, key_or_lock: str, lock: bool) -> list[int]:
        data = key_or_lock.split("\n")
        combination = []
        if not lock:
            data = data[::-1]
        data = data[1:]
        for col in range(len(data[0])):
            for row in range(len(data)):
                if data[row][col] != "#":
                    combination.append(row)
                    break
        return combination

    def count_fits(self) -> int:
        count = 0
        for lock in self.locks:
            for key in self.keys:
                for col in range(len(lock)):
                    if key[col] + lock[col] > 5:
                        break
                else:
                    count += 1
        return count

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    keys_and_locks = KeysAndLocks(input_data)
    number_fits = keys_and_locks.count_fits()
    print(f"The number of combinations of locks and keys that fit is {number_fits}")
