import re
from enum import Enum
from typing import Optional
from oooe.model.instruction import *

OPS = {
    'L[.]D',
    'MUL[.]D',
    'SUB[.]D',
    'DIV[.]D',
    'ADD[.]D',
    '[+]',
    '[-]',
    '[*]',
    '[/]'
}

class TokenType(Enum):
    WS = re.compile(r'\s+')
    COMMA = re.compile(r'[,]')
    INT = re.compile(r'\d+')
    L_PAREN = re.compile(r'\(')
    R_PAREN = re.compile(r'\)')
    REG = re.compile(r'[a-zA-Z]\d+|[([][a-zA-Z]\d+[])]')
    OP = re.compile('|'.join(OPS))
    ERROR = re.compile('')


class InstructionParser:
    def __init__(self, input_str: str=""):
        self._pos = 0
        self._tokens = []

    @property
    def tokens(self) -> list[tuple[TokenType, str]]:
        return self._tokens

    @property
    def pos(self) -> int:
        return self._pos

    def tokenize(self, input_str: str= ""):
        pos = 0
        self._tokens.clear()
        while pos < len(input_str):
            for token_type in TokenType:
                if match := token_type.value.match(input_str, pos):
                    if token_type == TokenType.ERROR:
                        raise ValueError(f'Invalid token at {pos}: {input_str[pos]}')
                    pos = match.end()
                    if token_type != TokenType.WS:
                        self._tokens.append((token_type, match.group(0)))
                    break

    def parse_instruction(self) -> Optional[Instruction]:
        self._pos = 0
        return self.parse_prefix_instruction()

    def parse_prefix_instruction(self):
        pos = self._pos
        next_type, next_label = self._tokens[self._pos]
        if next_type == TokenType.OP:
            self._pos += 1
            operands = self.parse_operands()
            if operands:
                if len(operands) == 2:
                    dest, src = operands
                    self._pos += 2
                    return MemoryInstruction(op=next_label, dest=dest, src=src)
                elif len(operands) == 3:
                    dest, src1, src2 = operands
                    self._pos += 3
                    return MathInstruction(op=next_label, dest=dest, src1=src1, src2=src2)
        self._pos = pos
        return None


    def parse_operands(self) -> Optional[list[Operand]]:
        operands = []
        if op := self.parse_operand():
            operands.append(op)

            while self._pos < len(self._tokens) and self._tokens[self._pos][0] == TokenType.COMMA:
                self._pos += 1
                if op := self.parse_operand():
                    operands.append(op)
                else:
                    return None
        else:
            return None
        return operands



    def parse_operand(self) -> Optional[Operand]:
        # Look ahead up to 4 tokens
        pos = self._pos
        match self._tokens[self._pos:self._pos + 4]:
            case [(TokenType.INT, offset),
                  (TokenType.L_PAREN, _),
                  (TokenType.REG, label),
                  (TokenType.R_PAREN, _)]:
                self._pos += 4
                return RegisterOperand(label=label, is_mem_reference=True, offset=int(offset))
            case [(TokenType.L_PAREN, _),
                  (TokenType.REG, label),
                  (TokenType.R_PAREN, _), *_]:
                self._pos += 3
                return RegisterOperand(label=label, is_mem_reference=True, offset=0)
            case [(TokenType.REG, label), *_]:
                self._pos += 1
                return RegisterOperand(label=label, is_mem_reference=False, offset=0)
        self._pos = pos
        return None

