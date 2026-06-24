from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable, Label

from oooe.model.instruction import Instruction
from oooe.model.processor import Processor
from oooe.parser import InstructionParser


class InstructionQueueView(VerticalScroll):
    data_table = reactive(DataTable())
    def __init__(self, processor: Processor):
        super().__init__()
        self.processor = processor

    def compose(self):
        yield Label("Instruction Queue")
        yield self.data_table

    def on_mount(self):
        self.data_table.add_columns("Op", "dest", "src1", "src2")

    def processor_updated(self):
        self.data_table.clear()

        for instruction in self.processor.instruction_queue:
            self.data_table.add_row(instruction.op, instruction.dest, *instruction.srcs)
        self.refresh()





