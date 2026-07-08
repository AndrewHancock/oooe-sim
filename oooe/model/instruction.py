from dataclasses import dataclass, field
from abc import ABC
from typing import List, Optional


@dataclass
class Operand(ABC):
    pass

@dataclass
class RegisterOperand(Operand):
    label: str
    is_mem_reference: bool = field(default=False)
    offset: Optional[int] = field(default=0)

    def __str__(self)-> str:
        result = self.label

        if self.is_mem_reference:
            result = '(' + result + ')'
            if self.offset:
                result = str(self.offset) + result
        return result

@dataclass
class MemoryOperand(Operand):
    base_register: RegisterOperand
    offset: RegisterOperand | LiteralOperand = field(default=None)


@dataclass()
class LiteralOperand(Operand):
    value: int

@dataclass()
class Instruction:
    op: str
    dest: RegisterOperand
    srcs: list[Operand]

    def __str__(self)-> str:
        return f'{self.op} {", ".join([self.dest].extend(self.srcs))}'