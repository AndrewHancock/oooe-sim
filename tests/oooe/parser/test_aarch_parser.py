import unittest

from oooe.model.instruction import RegisterOperand
from oooe.parser.aarch_parser import AArchParser


class test_parser(unittest.TestCase):
    def setUp(self):
        self.parser = AArchParser()

    def test_parse_register(self):
        input_str = "%rax"
        self.parser.tokenize(input_str)

        actual = self.parser.parse_register()

        expected = RegisterOperand(label="rax")

        self.assertEqual(expected, actual)