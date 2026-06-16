from textual.containers import VerticalScroll
from textual.widgets import DataTable

from oooe.model.instruction import MemoryInstruction, MathInstruction
from oooe.parser import InstructionParser


class InstructionQueue(VerticalScroll):
    def compose(self):
        yield self.get_instruction_queue()

    def get_instruction_queue(self) -> DataTable:
        t = DataTable()
        t.add_columns("Instr.", "dest", "src1", "src2")

        rows = []
        with open("input/long_example.s") as f:
            p = InstructionParser()
            for l in f.readlines():
                p.tokenize(l.strip())
                i = p.parse_instruction()
                match i:
                    case MemoryInstruction(op=op, dest=dest, src=src):
                        rows.append((op, dest, src, ""))
                    case MathInstruction(op=op, dest=dest, src1=src1, src2=src2):
                        rows.append((op, dest, src1, src2))
        t.add_rows(rows)
        return t