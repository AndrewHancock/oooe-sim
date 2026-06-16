from textual.containers import VerticalScroll
from textual.widgets import DataTable

from oooe.model.instruction import MemoryInstruction, MathInstruction
from oooe.model.processor import Processor
from oooe.parser import InstructionParser


class InstructionQueueView(VerticalScroll):
    def __init__(self, processor: Processor):
        super().__init__()
        self.processor = processor

    def compose(self):
        yield self.get_instruction_queue()

    def get_instruction_queue(self) -> DataTable:
        t = DataTable()
        t.add_columns("Instr.", "dest", "src1", "src2")
        for instruction in self.processor.instruction_queue:
            match instruction:
                case MemoryInstruction(op=op, dest=dest, src=src):
                    t.add_row(op, dest, src, None)
                case MathInstruction(op=op, dest=dest, src1=src1, src2=src2):
                    t.add_row(op, dest, src1, src2)
        return t




