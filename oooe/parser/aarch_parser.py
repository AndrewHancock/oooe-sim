import re
from enum import Enum
from typing import Optional

from oooe.model.instruction import Instruction, Operand, RegisterOperand

_OP_CODES = ['MOV', 'PUSH', 'CMP']
class Aarch64TokenType(Enum):
    OP = re.compile('[a-zA-z]+')
    PRECENT = re.compile('%')
    MINUS = re.compile('[-]')
    LPAREN = re.compile('[(]')
    RPAREN = re.compile('[)]')
    COMMA = re.compile(',')
    DOLLAR = re.compile('[$]')
    REGISTER = re.compile('[a-zA-Z_][a-zA-Z0-9]*')
    INT = re.compile(r'\d+')
    WS = re.compile(r'\s+')
    ERROR = re.compile('.')


def tokenize(input_str: str) -> list[tuple[Aarch64TokenType, str]]:
    pos = 0
    tokens = []
    while pos < len(input_str):
        for token_type in Aarch64TokenType:
            if match := token_type.value.match(input_str, pos):
                pos = match.end()
                if token_type == Aarch64TokenType.ERROR:
                    raise ValueError(f'Invalid token at {pos}: {input_str[pos]}')

                if token_type != Aarch64TokenType.WS:
                    tokens.append((token_type, match.group(0)))
                break
    return tokens

class Parser:
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
        if token_type == Aarch64TokenType.OP:
            self._pos += 1
            return token_str
        return None

    def parse_operands(self) -> list[Operand]:
        pass

    def parse_operand(self) -> Optional[Operand]:
        pass

    def parse_register(self) -> Optional[RegisterOperand]:
        offset = self.parse_offset()

        match self._tokens[self._pos:self._pos + 3]:
            case [(Aarch64TokenType.LPAREN, _), (Aarch64TokenType.OP, token_str), (Aarch64TokenType.RPAREN, _)]:
                self._pos += 3
                return RegisterOperand(label=token_str, is_mem_reference=True, offset=offset)
            case [(Aarch64TokenType.OP, token_str)]:
                self._pos += 1
                return RegisterOperand(label=token_str, is_mem_reference=False, offset=None)
            case _:
                return None


    def parse_offset(self) -> Optional[int]:
        pos = self._pos
        next_type, next_str = self._tokens[self._pos]
        negative = False
        if next_type == Aarch64TokenType.MINUS:
            negative = True
            self._pos += 1
            next_type, next_str = self._tokens[self._pos]

        if next_type == Aarch64TokenType.INT:
            self._pos += 1
            value = int(next_str)
            if negative:
                value = -value
            return value
        self._pos = pos
        return None




