from dataclasses import dataclass
from abc import ABC
import re


@dataclass
class Operand(ABC):
    label: str

@dataclass()
class RegisterOperand(Operand):
    is_mem_reference: bool
    offset: int

@dataclass()
class LiteralOperand(Operand):
    pass

@dataclass()
class Instruction(ABC):
    dest: RegisterOperand
    op: str
    pass

@dataclass()
class MathInstruction(Instruction):
    src1: Operand
    src2: Operand

@dataclass()
class MemoryInstruction(Instruction):
    src: Operand





p = InstructionParser()
print(p.parse_instruction('L.D F6, 34(R2)'))
print(p.parse_instruction('MUL.D F0, F2, F4'))