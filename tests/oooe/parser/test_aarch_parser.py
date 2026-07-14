import unittest

from oooe.model.instruction import RegisterOperand, LiteralOperand, MemoryOperand, Label
from oooe.parser.aarch_parser import AArchParser


class TestArchParser(unittest.TestCase):
    def setUp(self):
        self.parser = AArchParser()

    def test_parse_register(self):
        input_str = "x0"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_register()

        expected = RegisterOperand(label="x0")

        self.assertEqual(expected, actual)

    def test_parse_literal(self):
        input_str = "1254"

        self.parser.tokenize(input_str)

        actual = self.parser.parse_literal()
        expected = LiteralOperand(value=1254)
        self.assertEqual(expected, actual)

    def test_parse_immediate(self):
        input_str = "#1254"

        self.parser.tokenize(input_str)

        actual = self.parser.parse_literal()
        expected = LiteralOperand(value=1254)
        self.assertEqual(expected, actual)


    def test_parse_op_list_single(self):
        input_str = "x0"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_operand_list()
        expected = [RegisterOperand(label="x0")]
        self.assertEqual(expected, actual)

    def test_parse_op_list(self):
        input_str = "x0, 1, w2"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_operand_list()
        expected = [RegisterOperand(label="x0"), LiteralOperand(value=1), RegisterOperand(label="w2")]
        self.assertEqual(expected, actual)

    def test_parse_memory_base(self):
        input_str = "[x0]"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_memory_operand()
        expected = MemoryOperand(base_register=RegisterOperand(label="x0"))
        self.assertEqual(expected, actual)

    def test_parse_memory_base_offset_reg(self):
        input_str = "[x0, x1]"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_memory_operand()
        expected = MemoryOperand(base_register=RegisterOperand(label="x0"), offset=RegisterOperand(label="x1"))
        self.assertEqual(expected, actual)

    def test_parse_memory_base_offset_immediate(self):
        input_str = "[x0, 123]"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_memory_operand()
        expected = MemoryOperand(base_register=RegisterOperand(label="x0"), offset=LiteralOperand(value=123))
        self.assertEqual(expected, actual)

    def test_label(self):
        input_str = "some_label:"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_label()
        expected = Label(label="some_label")
        self.assertEqual(expected, actual)


