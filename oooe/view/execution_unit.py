from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Label, DataTable

from oooe.model.execution_unit import ExecutionUnit
from oooe.model.processor import Processor


class ExecutionUnitView(Vertical):

    def __init__(self, execution_unit: ExecutionUnit):
        super().__init__()
        self.execution_unit = execution_unit
        self.reservation_stations = DataTable()


    def compose(self) -> ComposeResult:
        yield Label("Execution Unit")
        yield Label(f"Supported Ops: {', '.join(self.execution_unit.op_times.keys())}")
        yield Label(f"Reservation Stations:")
        yield self.reservation_stations

    def on_mount(self):
        self.reservation_stations.add_columns("Name", "Op", "Val1", "Val2", "rs1", "rs2")

    def processor_updated(self):
        self.reservation_stations.clear()
        for rs in self.execution_unit.reservation_stations.values():
            self.reservation_stations.add_row(rs.name, rs.op, rs.val1, rs.val2, rs.rs1, rs.rs2)
