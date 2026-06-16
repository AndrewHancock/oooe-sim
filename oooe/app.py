from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual.containers import VerticalScroll

from oooe.widgets.instruction_queue import InstructionQueue

class OooeSimApp(App):
    CSS_PATH = "widgets/instruction_queue.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield InstructionQueue()

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    app = OooeSimApp()
    app.run()