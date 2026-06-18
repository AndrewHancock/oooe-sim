from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Collapsible, Label, collapsible

from oooe.model.processor import Processor


class RegisterView(Vertical):
    r_label = reactive(Label)
    f_label = reactive(Label)
    def __init__(self, processor: Processor):
        super().__init__()
        self.processor = processor

    def compose(self):
        with Collapsible(id="r_collapsible", title="Integer Registers"):
            yield self.r_label
        with Collapsible(id="F_collapsible", title="Floating Point Registers"):
            yield self.f_label

    def processor_updated(self):
        r_string = "\n".join([f"[bold]{k}[/bold] -> {v}" for k, v in self.processor.registers.isa_registers.items()])

        f_string = "\n".join([f"[bold]{k}[/bold] -> {v}" for k, v in self.processor.registers.isa_float_registers.items()])

        self.r_label.update(r_string)
        self.f_label.update(f_string)
