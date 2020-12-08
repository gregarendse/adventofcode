from typing import List, Set


class Data(object):
    accumulator: int = 0


class Instruction(object):

    def __init__(self, instruction: str, param: int) -> None:
        super().__init__()
        self.instruction = str(instruction)
        self.param = int(param)

    def __str__(self) -> str:
        return "{} {}".format(self.instruction, self.param)

    def execute(self, line: int = 0, data: Data = None) -> int:
        if "acc" == self.instruction:
            data.accumulator = data.accumulator + self.param
            return line + 1
        elif "jmp" == self.instruction:
            return line + self.param
        elif "nop" == self.instruction:
            return line + 1
        else:
            raise Exception("Unknown instruction: " + self.instruction)


def run(instructions: List[Instruction], data: Data = None) -> bool:
    _line: int = 0
    _executed_instructions: Set[Instruction] = set()

    while _line < len(instructions):
        _instruction: Instruction = instructions[_line]

        if len(_executed_instructions & {_instruction}) == 0:
            _executed_instructions.add(_instruction)
        else:
            return False

        _line = _instruction.execute(line=_line, data=data)

    return True


instructions: List[Instruction] = []

with open('input.txt', 'r') as input:
    for line in input.read().splitlines():
        parts = line.split()
        instructions.append(
            Instruction(
                str(parts[0]), int(parts[1])
            )
        )

data = Data()
run(instructions, data)
print(data.accumulator)

for i in range(len(instructions)):

    if instructions[i].instruction == "jmp":
        instructions[i].instruction = "nop"

        data = Data()
        if run(instructions, data):
            print(data.accumulator)
            break

        instructions[i].instruction = "jmp"

    if instructions[i].instruction == "nop":
        instructions[i].instruction = "jmp"

        data = Data()
        if run(instructions, data):
            print(data.accumulator)
            break

        instructions[i].instruction = "nop"

