import sys


def get_data_map(file_list: str) -> tuple[list[str], list[int]]:
    data_map = []
    length_per_id = []
    for index, element in enumerate(file_list):
        if index % 2 == 0:
            data_map.extend([str(index // 2)] * int(element))
            length_per_id.append(int(element))
        else:
            data_map.extend(["."] * int(element))
    return data_map, length_per_id


def get_checksum(data_map: list[str], move: bool = True) -> int:
    index_1 = 0
    index_2 = len(data_map) - 1
    checksum = 0
    if not move:
        while index_1 < len(data_map):
            if data_map[index_1] != ".":
                checksum += index_1 * int(data_map[index_1])
            index_1 += 1
        return checksum
    while index_1 <= index_2:
        if data_map[index_1] != ".":
            checksum += index_1 * int(data_map[index_1])
            index_1 += 1
        elif data_map[index_2] == ".":
            index_2 -= 1
        else:
            checksum += index_1 * int(data_map[index_2])
            index_1 += 1
            index_2 -= 1
    return checksum


def defragment_disk(data_map: list[str], length_per_id: list[int]) -> list[str]:
    current_file_id = int(data_map[-1])
    while current_file_id > 0:
        current_length = length_per_id[current_file_id]
        index = 0
        move_file = False
        while index < len(data_map):
            if data_map[index] == str(current_file_id):
                break
            if data_map[index] != ".":
                index += 1
                continue
            empty_legth = 0
            index_start = index
            while data_map[index] == ".":
                empty_legth += 1
                index += 1
            if empty_legth >= current_length:
                move_file = True
                break
        if not move_file:
            current_file_id -= 1
            continue
        for index in range(len(data_map)):
            if data_map[index] == str(current_file_id):
                data_map[index] = "."
        for index in range(current_length):
            data_map[index_start + index] = str(current_file_id)
        current_file_id -= 1
    return data_map


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    data_map, length_per_id = get_data_map(input_data)
    print(f"The checksum is {get_checksum(data_map)}")
    defragmented_disk = defragment_disk(data_map, length_per_id)
    print(f"After defracmentation, the checksum is {get_checksum(defragmented_disk, False)}")
