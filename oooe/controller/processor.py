from oooe.controller.action import Action
from oooe.controller.dispatch import issue
from oooe.model.processor import Processor


class ProcessorSim:
    def __init__(self, processor: Processor):
        self.clock_cycle = 0
        self.actions_by_clock: list[list[Action]]= []
        self.processor = processor

    def forward_clock(self):
        self.clock_cycle += 1

        if self.clock_cycle > len(self.actions_by_clock):
            actions = []
            if action := issue(self.processor):
                actions.append(action)
            self.actions_by_clock.append(actions)
        else:
            actions = self.actions_by_clock[self.clock_cycle - 1]

        for action in actions:
            action.do()

    def reverse_clock(self):
        if self.clock_cycle == 0:
            return

        self.clock_cycle -= 1
        for action in self.actions_by_clock[self.clock_cycle]:
            action.undo()







