from oooe.controller.action import Action
from oooe.model.execution_unit import ExecutionUnit
from oooe.model.processor import Processor


class IssueAction(Action):
    def __init__(self, exec_unit: ExecutionUnit, rs_name: str, op_time: int):
        super().__init__()
        self.exec_unit = exec_unit
        self.rs_name = rs_name
        self.op_time = op_time

    def do(self):
        self.exec_unit.executing_rs = self.rs_name
        self.exec_unit.cycles_remaining = self.op_time


    def undo(self):
        self.exec_unit.executing_rs = None
        self.exec_unit.cycles_remaining = None


def issue(processor: Processor) -> IssueAction | None:
    for exec_unit in processor.execution_units:
        if not exec_unit.executing_rs:
            for rs in exec_unit.reservation_stations.values():
                if rs.op and rs.val1 and not rs.rs1 and not rs.rs2:
                    return IssueAction(exec_unit, rs.name, exec_unit.op_times[rs.op])
    return None


