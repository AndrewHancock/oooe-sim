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
class Instruction():
    op: str
    dest: RegisterOperand
    srcs: list[Operand]

    def __str__(self)-> str:
        return f'{self.op} {", ".join([self.dest].extend(self.srcs))}'