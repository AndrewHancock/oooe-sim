from dataclasses import dataclass
from abc import ABC
from typing import List


@dataclass
class Operand(ABC):
    label: str

@dataclass()
class RegisterOperand(Operand):
    is_mem_reference: bool
    offset: int

    def __str__(self)-> str:
        result = self.label

        if self.is_mem_reference:
            result = '(' + result + ')'
            if self.offset:
                result = str(self.offset) + result
        return result

@dataclass()
class LiteralOperand(Operand):
    pass

@dataclass()
class Instruction(ABC):
    op: str
    dest: RegisterOperand
    pass

    def __str__(self)-> str:
        return f'{self.op} {self.dest}'

@dataclass()
class MathInstruction(Instruction):
    src1: Operand
    src2: Operand

    def __str__(self) -> str:
        return f'{self.op} {self.dest}, {self.src1}, {self.src2}'

@dataclass()
class MemoryInstruction(Instruction):
    src: Operand

    def __str__(self)-> str:
        return f'{self.op} {self.dest}, {self.src}'


