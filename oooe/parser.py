import re
from instruction import *

# Convenient regex for parsing
OPS = re.compile(r'L[.]D|MUL.D|SUB.D|DIV.D|ADD.D')
WS = re.compile(r'\s+')
COMMA = re.compile(r'[,]')
INT = re.compile(r'\d+')
REG = re.compile(r'[a-zA-Z]\d+')


class InstructionParser:
    def __init__(self):
        self._pos = None
        self._input_str = None

    def parse_instruction(self, input_str: str) -> Instruction:
        self._input_str = input_str
        self._pos = 0
        self.eat_ws()

        match = OPS.match(self._input_str)
        if not match:
            raise ValueError(f'Invalid instruction: {self._input_str}')
        op = match.group(0)
        self._pos = match.end()
        self.eat_ws()

        operands = self.parse_operands()

        if op == 'L.D' and len(operands) == 2:
            dest, src = operands
            return MemoryInstruction(op=op, dest=dest, src=src)
        elif len(operands) == 3:
            dest, src1, src2 = operands
            return MathInstruction(op=op, dest=dest, src1=src1, src2=src2)
        else:
            raise ValueError(f'Invalid instruction: {self._input_str}')

    def eat_ws(self):
        match = WS.match(self._input_str, self._pos)
        if match:
            self._pos = match.end()


    def parse_operands(self) -> list[Operand]:
       result = [self.parse_operand()]
       while match := COMMA.match(self._input_str, self._pos):
           self._pos = match.end()
           self.eat_ws()
           result.append(self.parse_operand())
       return result


    def parse_operand(self) -> Operand:
        int_prefix = 0
        in_paren = False
        match = INT.match(self._input_str, self._pos)
        if match:
            int_prefix = match.group(0)
            self._pos = match.end()
        if self._input_str[self._pos] == '(':
            in_paren = True
            self._pos += 1

        match = REG.match(self._input_str, self._pos)
        if match:
            label = match.group(0)
            self._pos = match.end()

            if in_paren and len(self._input_str) > self._pos and \
                    (self._input_str[self._pos]  != ')' or not in_paren and self._input_str[self._pos] == ')'):
                raise ValueError(f'Invalid instruction: {self._input_str}')
            if in_paren:
                self._pos += 1
                return RegisterOperand(label=label, is_mem_reference=True, offset=int_prefix)
            else:
                return RegisterOperand(label=label, is_mem_reference=False, offset=int_prefix)
        else:
            raise ValueError(f'Invalid instruction: {self._input_str}')