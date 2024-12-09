import sys


class File:
    def __init__(self, id: int, size: int, location: int) -> None:
        self.id = id
        self.size = size
        self.location = location
        self.end_location = location + size

    def checksum_value(self) -> int:
        return sum(
            [
                index * self.id
                for index in range(self.location, self.location + self.size)
            ]
        )

    def update_location(self, location: int):
        self.location = location
        self.end_location = location + self.size


class FreeSpace:
    def __init__(self, size: int, location: int) -> None:
        self.size = size
        self.location = location


class FileSystem:
    def __init__(self, file_list: str) -> None:
        self.files = []
        self.empty = []
        location = 0
        for index, element in enumerate(file_list):
            length = int(element)
            if index % 2 == 0:
                self.files.append(File(index // 2, length, location))
            else:
                self.empty.append(FreeSpace(length, location))
            location += length

    def __repr__(self) -> str:
        self.files.sort(key=lambda file: file.location)
        files = ""
        for file in self.files:
            files += "." * (file.location - len(files))
            files += str(file.id) * file.size
        return files

    def degrafment(self) -> None:
        for file_index in range(len(self.files) - 1, 0, -1):
            file_size = self.files[file_index].size
            for empty_index in range(len(self.empty)):
                if self.empty[empty_index].location > self.files[file_index].location:
                    break
                empty_size = self.empty[empty_index].size
                if file_size <= empty_size:
                    self.files[file_index].update_location(
                        self.empty[empty_index].location
                    )
                    if file_size == empty_size:
                        self.empty.pop(empty_index)
                    else:
                        self.empty[empty_index].location = self.files[
                            file_index
                        ].end_location
                        self.empty[empty_index].size = empty_size - file_size
                    break

    def checksum(self, move: bool = True) -> int:
        index_1 = 0
        checksum = 0
        if not move:
            for file in self.files:
                checksum += file.checksum_value()
            return checksum
        index_2 = len(self.files) - 1
        remaining_late = self.files[index_2].size
        while index_1 < index_2:
            checksum += self.files[index_1].checksum_value()
            next_empty = (
                self.files[index_1 + 1].location - self.files[index_1].end_location
            )
            start_index_empty = self.files[index_1].location + self.files[index_1].size
            index_1 += 1
            if next_empty == 0:
                continue
            for index in range(next_empty):
                checksum += self.files[index_2].id * (start_index_empty + index)
                remaining_late -= 1
                if remaining_late == 0:
                    index_2 -= 1
                    remaining_late = self.files[index_2].size
        if remaining_late == 0:
            checksum += self.files[index_2].checksum_value()
        else:
            for index in range(remaining_late):
                checksum += self.files[index_2].id * (
                    self.files[index_2].location + index
                )
        return checksum


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    input_data = open(file_name).read().strip()
    file_system = FileSystem(input_data)
    print(f"The checksum is {file_system.checksum(True)}")
    file_system.degrafment()
    print(f"After defragmenting, it's {file_system.checksum(False)}")
