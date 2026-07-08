import re
from enum import Enum
from typing import Optional

from oooe.model.instruction import Instruction, Operand, RegisterOperand, LiteralOperand, MemoryOperand
from oooe.parser.aarm64_isa import _ARM64_OPCODES, _ARM64_REGISTERS


class AArchTokenType(Enum):
    OP = re.compile('|'.join(sorted(_ARM64_OPCODES)), flags=re.IGNORECASE)
    LBRACKET = re.compile(r'\[')
    RBRACKET = re.compile(r']')
    COMMA = re.compile(',')
    REGISTER = re.compile('|'.join(sorted(_ARM64_REGISTERS)), flags=re.IGNORECASE)
    LABEL = re.compile('[.a-zA-Z_][.a-zA-Z0-9_]*')
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

    def parse_instructions(self, input_str: str):
        self._pos = 0
        self._tokens = tokenize(input_str)

    def parse_instruction(self) -> Optional[Instruction]:
        op_code = self.parse_op_code()

        if op_code:
            pass
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







        self._pos = pos
        return None


    def parse_literal(self) -> Optional[LiteralOperand]:
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








