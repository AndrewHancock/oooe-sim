from dataclasses import dataclass, field
from abc import ABC
from typing import List, Optional

@dataclass
class Label:
    label: str


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

    def __str__(self)-> str:
        result = f'[{str(self.base_register)}'
        if self.offset:
            result += f", {str(self.offset)}"
        result += ']'
        return result


@dataclass()
class LiteralOperand(Operand):
    value: int

    def __str__(self)-> str:
        return str(self.value)

@dataclass()
class Instruction:
    op_code: str
    operands: Optional[list[Operand | Label]]

    def __str__(self)-> str:
        result = self.op_code
        if self.operands:
            result += " "
            result += ", ".join(str(s) for s in self.operands)

        return result