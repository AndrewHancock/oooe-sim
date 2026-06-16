from oooe.controller.action import Action
from oooe.model import processor
from oooe.model.instruction import Instruction
from oooe.model.processor import Processor

class DispatchAction(Action):
    def __init__(self, processor: Processor, target_rs_name: str):
        self._processor = processor
        self._target_rs_name = target_rs_name
        self._instruction = None
        self._old_rs_entry

    def do(self):
        self._instruction = self._processor.instruction_queue.pop(0)
        for ex_unit in self._processor.execution_units:
            if self._target_rs_name in ex_unit.reservation_stations:
                rs = ex_unit.reservation_stations[self._target_rs_name]
                match self._instruction:
                    case MemoryInstruction(op=op, dest=dest, src=src):
                        new_rs = rs.replace(op=op, dest=dest, )









def dispatch(p: Processor) -> list[Action]:
    ins = p.instruction_queue[0]
    for ex_unit in p.execution_units:
        if ins.op in ex_unit.op_times.keys():
            for rs in ex_unit.reservation_stations:
                if not rs.op:
                    return DispatchAction(p)
    return None


