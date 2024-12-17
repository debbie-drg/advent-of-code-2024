import sys


class TernaryMachine:
    def __init__(self, register_values: str) -> None:
        split_values = register_values.split("\n")
        self.register_A = int(split_values[0].split()[-1])
        self.register_B = int(split_values[1].split()[-1])
        self.register_C = int(split_values[2].split()[-1])

    def __repr__(self) -> str:
        return f"Ternary machine with {self.register_A} in A, {self.register_B} in B, {self.register_C} in C"

    def perform_instructions(
        self, instructions: str, parse_str: bool = True
    ) -> list[int] | str:
        instruction_list = [
            int(element) for element in instructions.split(" ")[1].split(",")
        ]
        output = []
        tape_position = 0
        while tape_position < len(instruction_list):
            move_tape_to = None
            literal_operand = instruction_list[tape_position + 1]
            combo_operand = self.combo_operand(instruction_list[tape_position + 1])
            match instruction_list[tape_position]:
                case 0:
                    self.register_A = self.register_A // (2**combo_operand)
                case 1:
                    self.register_B = self.register_B ^ literal_operand
                case 2:
                    self.register_B = combo_operand % 8
                case 3:
                    if self.register_A != 0:
                        move_tape_to = literal_operand
                case 4:
                    self.register_B = self.register_B ^ self.register_C
                case 5:
                    output.append(combo_operand % 8)
                case 6:
                    self.register_B = self.register_A // (2**combo_operand)
                case 7:
                    self.register_C = self.register_A // (2**combo_operand)
                case _:
                    raise ValueError
            if move_tape_to is not None:
                tape_position = move_tape_to
            else:
                tape_position += 2
        if parse_str:
            return ",".join([str(element) for element in output])
        return output

    def combo_operand(self, combo_operand: int) -> int:
        if combo_operand <= 3:
            return combo_operand
        try:
            return [self.register_A, self.register_B, self.register_C][
                combo_operand - 4
            ]
        except IndexError:
            return 7

    def find_self_output(
        self, instructions, A_value=0, current_length: int = 1
    ) -> int | None:
        # The key realisation is that in each loop through the instructions, the contents of register
        # A are divided by 8. Therefore we can try to go right to left, finding the correct end and 
        # multiplying by 8 going one level up to the next digit.
        to_compare = [int(element) for element in instructions.split(" ")[1].split(",")]
        if current_length == len(to_compare) + 1:
            return A_value
        for index in range(8):
            self.register_A = A_value * 8 + index
            output = self.perform_instructions(instructions, False)
            if output == to_compare[-current_length:]:
                next_value = self.find_self_output(
                    instructions, A_value * 8 + index, current_length + 1
                )
                if next_value:
                    return next_value


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    registers, instructions = open(file_name).read().strip().split("\n\n")
    ternary_machine = TernaryMachine(registers)
    output = ternary_machine.perform_instructions(instructions)
    print(f"The program output is {output}")
    lowest_value = ternary_machine.find_self_output(instructions)
    ternary_machine.register_A = lowest_value
    print(
        f"The lowest index for which the program outputs itself is {ternary_machine.find_self_output(instructions)}"
    )
