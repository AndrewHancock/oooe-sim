import unittest
from oooe.parser import *


class TestParser(unittest.TestCase):
    def test_tokenize(self):
        p = InstructionParser()
        p.tokenize("R1 R2,LD.D,123 123(F1)")
        actual = p.tokens
        expected = [(TokenType.REG, 'R1'), (TokenType.REG, 'R2'), (TokenType.COMMA, ','), (TokenType.OP, 'LD.D'),
                    (TokenType.COMMA, ','), (TokenType.INT, '123'), (TokenType.INT, '123'),
                    (TokenType.L_PAREN, '('),(TokenType.REG, 'F1'), (TokenType.R_PAREN, ')')]

        self.assertEqual(actual, expected)

    def test_tokenize_neg(self):
        p = InstructionParser()
        with self.assertRaises(ValueError):
            p.tokenize("R1 LD.D ? F2 MUL.D")

    def test_parse_basic_reg_opearnd(self):
        p = InstructionParser()
        p.tokenize("R1")
        actual = p.parse_operand()
        expected = RegisterOperand(label='R1', is_mem_reference=False, offset=0)
        self.assertEqual(actual, expected)

        self.assertEqual(p.pos, 1)

    def test_parse_mem_operand_no_offset(self):
        p = InstructionParser()
        p.tokenize("(R1)")
        actual = p.parse_operand()
        expected = RegisterOperand(label='R1', is_mem_reference=True, offset=0)
        self.assertEqual(expected, actual)

    def test_parse_mem_operand_with_offset(self):
        p = InstructionParser()
        p.tokenize("123(R1)")
        actual = p.parse_operand()
        expected = RegisterOperand(label='R1', is_mem_reference=True, offset=123)
        self.assertEqual(expected, actual)

    def test_parse_operands(self):
        p = InstructionParser()
        p.tokenize("(R1), R2, 789(F3)")
        actual = p.parse_operands()
        expected = [RegisterOperand(label='R1', is_mem_reference=True, offset=0),
                    RegisterOperand(label='R2', is_mem_reference=False, offset=0),
                    RegisterOperand(label='F3', is_mem_reference=True, offset=789)]

        self.assertEqual(expected, actual)

    def test_parse_operands_neg(self):
        p = InstructionParser()
        p.tokenize("(R1), R2, 789(F3),")
        actual = p.parse_operands()

        self.assertEqual(None, actual)

    def test_parse_prefix_mem_instruction(self):
        p = InstructionParser()
        p.tokenize("LD.D F6, 34(R2)")
        actual = p.parse_instruction()
        expected = MemoryInstruction(op='LD.D',
                                     dest=RegisterOperand(label='F6', is_mem_reference=False, offset=0),
                                     src=RegisterOperand(label='R2', is_mem_reference=True, offset=34))
        self.assertEqual(expected, actual)

    def test_parse_prefix_math_instruction(self):
        p = InstructionParser()
        p.tokenize("MUL.D F6, F12, 34(R2)")
        actual = p.parse_instruction()
        expected = MathInstruction(op='MUL.D',
                                     dest=RegisterOperand(label='F6', is_mem_reference=False, offset=0),
                                     src1=RegisterOperand(label='F12', is_mem_reference=False, offset=0),
                                     src2=RegisterOperand(label='R2', is_mem_reference=True, offset=34))
        self.assertEqual(expected, actual)


