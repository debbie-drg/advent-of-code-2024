import sys
from copy import copy
from collections import defaultdict


class MonitoringDevice:
    def __init__(self, register_values: str, instructions: str) -> None:
        self.registers = dict()
        for line in register_values.split("\n"):
            name, value = line.split(": ")
            self.registers[name] = bool(int(value))
        split_instructions = [
            operation.split() for operation in instructions.split("\n")
        ]
        self.instructions = []
        self.gates_to_operations = defaultdict(list)
        for index, instruction in enumerate(split_instructions):
            in_registers = {instruction[0], instruction[2]}
            op = instruction[1]
            destination = instruction[4]
            self.instructions.append((in_registers, op, destination))
            self.gates_to_operations[frozenset(in_registers)].append(index)

    def operation(
        self, register_1: str, register_2: str, op: str, destination: str
    ) -> bool:
        if not register_1 in self.registers or not register_2 in self.registers:
            return False
        value_1, value_2 = self.registers[register_1], self.registers[register_2]
        match op:
            case "AND":
                result = value_1 & value_2
            case "OR":
                result = value_1 | value_2
            case "XOR":
                result = value_1 ^ value_2
            case _:
                raise ValueError
        self.registers[destination] = result
        return True

    def run(self):
        queue = copy(self.instructions)
        while queue:
            registers, op, destination = queue.pop(0)
            register_1 = registers.pop()
            register_2 = registers.pop()
            if not self.operation(register_1, register_2, op, destination):
                queue.append(({register_1, register_2}, op, destination))

    def get_number(self) -> int:
        number = ""
        zregisters = sorted(
            [register for register in self.registers if register.startswith("z")]
        )
        for register in zregisters:
            number += "1" if self.registers[register] else "0"
        return int(number[::-1], 2)

    def find_output(self, input_1: str, input_2: str, operator: str) -> str | None:
        nodes = frozenset({input_1, input_2})
        if nodes not in self.gates_to_operations:
            return None
        for index in self.gates_to_operations[nodes]:
            instruction = self.instructions[index]
            if instruction[1] == operator:
                return instruction[2]

    def check_block(
        self, x: str, y: str, last_carry: str | None
    ) -> tuple[str | None, str | None, list[str]]:

        to_swap = []

        inter_sum = self.find_output(x, y, "XOR")

        if not inter_sum:
            raise ValueError

        inter_carry = self.find_output(x, y, "AND")

        if not inter_carry:
            raise ValueError

        if last_carry is not None:
            inter_sum_carry = self.find_output(last_carry, inter_sum, "AND")
            if not inter_sum_carry:
                inter_carry, inter_sum = inter_sum, inter_carry
                to_swap.extend([inter_sum, inter_carry])
                inter_sum_carry = self.find_output(last_carry, inter_sum, "AND")

            output = self.find_output(last_carry, inter_sum, "XOR")

            if inter_sum and inter_sum.startswith("z"):
                inter_sum, output = output, inter_sum
                to_swap.extend([inter_sum, output])

            if inter_carry and inter_carry.startswith("z"):
                inter_carry, output = output, inter_carry
                to_swap.extend([inter_carry, output])

            if inter_sum_carry and inter_sum_carry.startswith("z"):
                inter_sum_carry, output = output, inter_sum_carry
                to_swap.extend([inter_sum_carry, output])

            if not inter_sum_carry or not inter_carry:
                raise ValueError
            
            next_carry = self.find_output(inter_sum_carry, inter_carry, "OR")
        else:
            output = inter_sum
            next_carry = inter_carry

        return output, next_carry, to_swap

    def find_swaps(self) -> str:
        bits = max(
            [
                int(register.removeprefix("x"))
                for register in self.registers
                if register.startswith("x")
            ]
        )
        last_carry = None
        swap = []
        for index in range(bits):
            value = "0" + str(index) if index < 10 else str(index)
            input_1, input_2 = f"x{value}", f"y{value}"
            output, next_carry, swapped = self.check_block(input_1, input_2, last_carry)
            swap.extend(swapped)

            if next_carry and next_carry.startswith("z") and next_carry != f"z{bits}":
                output, next_carry = next_carry, output
                swap.extend([output, next_carry])

            last_carry = (
                next_carry if next_carry else self.find_output(input_1, input_2, "AND")
            )

        return ",".join(sorted(swap))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    register_values, instructions = open(file_name).read().strip().split("\n\n")
    monitoring_device = MonitoringDevice(register_values, instructions)
    monitoring_device.run()
    result = monitoring_device.get_number()
    print(f"The number in the z registers is {result}")
    print(f"The swapped wires are {monitoring_device.find_swaps()}")
