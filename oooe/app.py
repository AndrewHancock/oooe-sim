import sys

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import VerticalScroll, Horizontal, Vertical

from oooe.controller.processor import ProcessorSim
from oooe.model.processor import Processor, get_processor
from oooe.parser import get_instructions
from oooe.view.clock import ClockCycleView
from oooe.view.execution_unit import ExecutionUnitView
from oooe.view.instruction_queue import InstructionQueueView
from oooe.view.register_allocation_table import RegisterAllocationTableView
from oooe.view.registers import RegisterView


class OooeSimApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("f", "forward_clock", "Forward one clock cycle"),
                ("r", "reverse_clock", "Reverse one clock cycle")]


    def __init__(self, processor: Processor, processor_sim: ProcessorSim):
        super().__init__()
        self._processor = processor
        self._processor_sim = processor_sim

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            with Horizontal():
                yield ClockCycleView(id="clock_cycle")
                yield InstructionQueueView(self._processor)
                yield RegisterAllocationTableView(self._processor)
                yield RegisterView(self._processor)
            with Horizontal():
                for ex_unit in self._processor.execution_units:
                    yield ExecutionUnitView(ex_unit)
    def on_mount(self):
        self.processor_updated()

    def processor_updated(self):
        self.query_one(ClockCycleView).clock_cycle = self._processor_sim.clock_cycle
        self.query_one(InstructionQueueView).processor_updated()
        self.query_one(RegisterView).processor_updated()
        self.query_one(RegisterAllocationTableView).processor_updated()
        for ex_unit_vw in self.query(ExecutionUnitView):
            ex_unit_vw.processor_updated()
        self.refresh()

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_forward_clock(self):
        self._processor_sim.forward_clock()
        self.processor_updated()

    def action_reverse_clock(self):
        self._processor_sim.reverse_clock()
        self.processor_updated()



if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "../input/long_example.s"
    instructions = get_instructions(input_path)
    p = get_processor(instructions)
    sim = ProcessorSim(p)
    app = OooeSimApp(p, sim)
    app.run()