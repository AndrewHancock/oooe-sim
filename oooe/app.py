import sys

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import VerticalScroll, Horizontal

from oooe.model.processor import Processor, get_processor
from oooe.parser import get_instructions
from oooe.view.execution_unit import ExecutionUnitView
from oooe.view.instruction_queue import InstructionQueueView

class OooeSimApp(App):
    CSS_PATH = "view/instruction_queue.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, processor: Processor):
        super().__init__()
        self._processor = processor

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield InstructionQueueView(self._processor)
        with Horizontal():
            for ex_unit in self._processor.execution_units:
                yield ExecutionUnitView(ex_unit)

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "../input/long_example.s"
    instructions = get_instructions(input_path)
    p = get_processor(instructions)
    app = OooeSimApp(p)
    app.run()