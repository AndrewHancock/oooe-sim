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
    op: str
    dest: RegisterOperand
    pass

@dataclass()
class MathInstruction(Instruction):
    src1: Operand
    src2: Operand

@dataclass()
class MemoryInstruction(Instruction):
    src: Operand
