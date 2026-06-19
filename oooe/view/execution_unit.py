from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Label, DataTable, ProgressBar

from oooe.model.execution_unit import ExecutionUnit
from oooe.model.processor import Processor


class ExecutionUnitView(Vertical):

    def __init__(self, execution_unit: ExecutionUnit):
        super().__init__()
        self.execution_unit = execution_unit
        self.reservation_stations = DataTable()
        self.progress_bar = ProgressBar()


    def compose(self) -> ComposeResult:
        yield Label("Execution Unit")
        yield Label(f"Supported Ops: {', '.join(self.execution_unit.op_times.keys())}")
        yield Label(f"Reservation Stations:")
        with Vertical(id="execution_unit"):
            yield Label("Idle", id="execution_text")
        yield self.reservation_stations

    def on_mount(self):
        self.reservation_stations.add_columns("Name", "Op", "Val1", "Val2", "rs1", "rs2")

    def processor_updated(self):
        self.reservation_stations.clear()
        first = True

        for rs in self.execution_unit.reservation_stations.values():
            if exec_rs := self.execution_unit.executing_rs and first:
                first = False

                rs_entry = (rs.name, rs.op, rs.val1, rs.val2, rs.rs1, rs.rs2)
                styled_row = [
                    Text(str(cell), style="background: blue") for cell in rs_entry
                ]
                self.reservation_stations.add_row(*styled_row)
            else:
                self.reservation_stations.add_row(rs.name, rs.op, rs.val1, rs.val2, rs.rs1, rs.rs2, key=rs.name)


        if exec_rs := self.execution_unit.executing_rs:
            exec_unit = self.execution_unit
            vert = self.query_one("#execution_unit")
            vert.styles.background = "darkgreen"

            label = self.query_one("#execution_text")
            label.content= f"{exec_unit.reservation_stations[exec_rs].op}\nCycles Remaining: {exec_unit.cycles_remaining}"
        else:
            vert = self.query_one("#execution_unit")
            vert.styles.background = "black"

            label = self.query_one("#execution_text")
            label.content = f"Idle"



