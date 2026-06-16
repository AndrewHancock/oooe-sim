from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, DataTable

from oooe.model.execution_unit import ExecutionUnit
from oooe.model.processor import Processor


class ExecutionUnitView(Vertical):
    def __init__(self, execution_unit: ExecutionUnit):
        super().__init__()
        self.execution_unit = execution_unit


    def compose(self) -> ComposeResult:
        yield Label("Execution Unit")
        yield self.get_reservation_stations()

    def get_reservation_stations(self):
        t = DataTable()
        t.add_columns("Name", "Op", "Val1", "Val2", "rs1", "rs2")

        for rs in self.execution_unit.reservation_stations.values():
            t.add_row(rs.name, None, None, None, None, None)
        return t