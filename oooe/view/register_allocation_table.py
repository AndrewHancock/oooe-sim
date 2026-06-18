from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import DataTable, Label

from oooe.model.processor import Processor


class RegisterAllocationTableView(Vertical):
    data_table = DataTable()
    def __init__(self, processor: Processor):
        super().__init__()
        self._processor = processor

    def compose(self) -> ComposeResult:
        yield Label("Register Allocation Table")
        yield self.data_table
        
    def on_mount(self):
        self.data_table.add_columns("Reg", "RS Name")

    def processor_updated(self):
        self.data_table.clear()

        self.data_table.add_rows(self._processor.registers.register_allocation_table.items())
        self.refresh()





