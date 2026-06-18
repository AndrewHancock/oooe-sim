from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable

from oooe.model.instruction import MemoryInstruction, MathInstruction
from oooe.model.processor import Processor
from oooe.parser import InstructionParser


class InstructionQueueView(VerticalScroll):
    data_table = reactive(DataTable())
    def __init__(self, processor: Processor):
        super().__init__()
        self.processor = processor

    def compose(self):
        yield self.data_table

    def processor_updated(self):
        self.data_table.clear()
        self.data_table.add_columns("Op", "dest", "src1", "src2")
        for instruction in self.processor.instruction_queue:
            match instruction:
                case MemoryInstruction(op=op, dest=dest, src=src):
                    self.data_table.add_row(op, dest, src, None)
                case MathInstruction(op=op, dest=dest, src1=src1, src2=src2):
                    self.data_table.add_row(op, dest, src1, src2)
        self.refresh()





