from textual.containers import Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Digits


class ClockCycleView(Vertical):
    clock_cycle = reactive(0)

    def compose(self):
        yield Digits()

    def watch_clock_cycle(self):
        digits = self.query_one(Digits)
        digits.update(str(self.clock_cycle))