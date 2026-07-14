import re
import sys
from enum import Enum
from io import TextIOBase
from typing import Optional, TextIO

from oooe.model.instruction import Instruction, Operand, RegisterOperand, LiteralOperand, MemoryOperand, Label
from oooe.model.program import Program
from oooe.parser.aarm64_isa import _ARM64_OPCODES, _ARM64_REGISTERS


class AArchTokenType(Enum):
    OP = re.compile('|'.join(sorted(_ARM64_OPCODES)), flags=re.IGNORECASE)
    LBRACKET = re.compile(r'\[')
    RBRACKET = re.compile(r']')
    COMMA = re.compile(',')
    COLON = re.compile(':')
    HASH = re.compile('#')
    REGISTER = re.compile('|'.join(sorted(_ARM64_REGISTERS)), flags=re.IGNORECASE)
    LABEL = re.compile('[.a-zA-Z_][.a-zA-Z0-9_()*, ]*')
    INT = re.compile(r'\d+')
    WS = re.compile(r'\s+')
    ERROR = re.compile('.')


def tokenize(input_str: str) -> list[tuple[AArchTokenType, str]]:
    pos = 0
    tokens = []
    while pos < len(input_str):
        for token_type in AArchTokenType:
            if match := token_type.value.match(input_str, pos):
                pos = match.end()
                if token_type == AArchTokenType.ERROR:
                    raise ValueError(f'Invalid token at {pos}: {input_str[pos]}')

                if token_type != AArchTokenType.WS:
                    tokens.append((token_type, match.group(0)))
                break
    return tokens

class AArchParser:
    def __init__(self):
        self._pos = 0
        self._tokens = None

    def tokenize(self, input_str: str):
        self._pos = 0
        self._tokens = tokenize(input_str)

    def parse_label_or_instruction(self) -> Optional[Instruction | Label]:
        return self.parse_label() or self.parse_instruction()

    def parse_label(self) -> Optional[Label]:
        next_type, label_str = self._tokens[self._pos]
        if next_type == AArchTokenType.LABEL and self._pos + 1 < len(self._tokens):
            self._pos += 1
            next_type, _ = self._tokens[self._pos]
            if next_type == AArchTokenType.COLON:
                self._pos += 1
                return Label(label=label_str)
        return None

    def parse_instruction(self) -> Optional[Instruction]:
        op_code = self.parse_op_code()
        if op_code:
            operands = None
            if self._pos < len(self._tokens):
                operands = self.parse_operand_list()
            return Instruction(op_code=op_code, operands=operands)
        else:
            return None


    def parse_op_code(self) -> Optional[str]:
        token_type, token_str = self._tokens[self._pos]
        if token_type == AArchTokenType.OP:
            self._pos += 1
            return token_str
        return None

    def parse_operands(self) -> list[Operand]:
        pass

    def parse_operand(self) -> Optional[Operand]:
        return self.parse_register() or self.parse_literal() or self.parse_memory_operand()


    def parse_register(self) -> Optional[RegisterOperand]:
        next_type, next_str = self._tokens[self._pos]
        if next_type == AArchTokenType.REGISTER:
            self._pos += 1
            return RegisterOperand(label=next_str)
        else:
            return None

    def parse_memory_operand(self) -> Optional[MemoryOperand]:
        pos = self._pos
        next_type, _ = self._tokens[self._pos]
        if next_type == AArchTokenType.LBRACKET:
            self._pos += 1
            operands = self.parse_operand_list()
            next_type, _ = self._tokens[self._pos]
            if next_type == AArchTokenType.RBRACKET:
                match operands:
                    case [RegisterOperand() as base]:
                        return MemoryOperand(base_register=base)
                    case [RegisterOperand() as base, LiteralOperand() | RegisterOperand() as offset]:
                        return MemoryOperand(base_register=base, offset=offset)
        self._pos = pos
        return None

    def parse_literal(self) -> Optional[LiteralOperand]:
        pos = self._pos
        next_type, next_str = self._tokens[self._pos]

        # Immediates preceded by a #, but we treat them the same.
        if next_type == AArchTokenType.HASH:
            self._pos += 1
            next_type, next_str = self._tokens[self._pos]

        if next_type == AArchTokenType.INT:
            self._pos += 1
            return LiteralOperand(value=int(next_str))
        else:
            return None

    def parse_operand_list(self) -> Optional[list[Operand]]:
        pos = self._pos
        first = self.parse_operand()
        if first:
            result = [first]
            while  self._pos < len(self._tokens) and self._tokens[self._pos][0] == AArchTokenType.COMMA:
                self._pos += 1
                if op := self.parse_operand():
                    result.append(op)
                else:
                    self._pos = pos
                    return None
            return result
        else:
            self._pos = pos
            return None


def parse_program(input_stream: TextIOBase) -> Program:
    parser = AArchParser()
    program = Program()
    for i, line in enumerate(input_stream):
        parser.tokenize(line)
        match parser.parse_label_or_instruction():
            case Label() as label:
                program.label_address_map[label.label] = i
            case Instruction() as instruction:
                program.instructions.append(instruction)
            case _:
                raise ValueError(f'Invalid instruction at {line}: {i}')
    return program


if __name__ == '__main__':
    with open('../../input/arm64_example.s') as f:
        p = parse_program(f)

        line_labels = {v: k for k, v in p.label_address_map.items()}

        for i, instruction in enumerate(p.instructions):
            if i in line_labels:
                print(f'{line_labels[i]}:')
            else:
                print(f'\t{str(instruction)}')









