from oooe.controller.action import Action
from oooe.model.execution_unit import ExecutionUnit
from oooe.model.instruction import Instruction, MemoryInstruction, MathInstruction
from oooe.model.processor import Processor
from oooe.model.reservation_station import ReservationStation
from dataclasses import replace


class IssueAction(Action):
    def __init__(self, processor: Processor, execution_unit: ExecutionUnit, target_rs_name: str):
        super().__init__()
        self._processor = processor
        self._ex_unit = execution_unit
        self._target_rs_name = target_rs_name
        self._instruction = None
        self._old_rs_entry = None
        self._has_old_rat_entry = None
        self._old_rat_entry = None


    def do(self):
        super().do()
        # Pop instruction off the queue
        self._instruction = self._processor.instruction_queue.pop(0)

        # Update RAT, saving old RAT entry if it exists
        self._has_old_rat_entry = self._instruction.dest.label in self._processor.registers.register_allocation_table
        if self._has_old_rat_entry:
            self._old_rat_entry = self._processor.registers.register_allocation_table[self._instruction.dest.label]
        self._processor.registers.update_rat_entry(self._instruction.dest.label, self._target_rs_name)

        # Update reservation station, saving old reservation station entry
        rs = self._ex_unit.reservation_stations[self._target_rs_name]
        self._old_rs_entry = rs
        self._processor.registers.update_rat_entry(self._instruction.dest.label, rs.name)
        new_rs = self.get_rs_for_instruction(self._instruction, rs)
        self._ex_unit.reservation_stations[self._target_rs_name] = new_rs


    def undo(self):
        super().undo()
        self._processor.instruction_queue.insert(0, self._instruction)
        self._ex_unit.reservation_stations[self._target_rs_name] = self._old_rs_entry
        if not self._has_old_rat_entry:
            self._processor.registers.remove_rat_entry(self._instruction.dest.label)
        else:
            self._processor.registers.update_rat_entry(self._instruction.dest.label, self._old_rat_entry)

    def get_rs_for_instruction(self, instruction: Instruction, src_rs) -> ReservationStation:
        _op = instruction.op
        reg = self._processor.registers
        val2 = None
        rs2 = None
        match instruction:
            case MemoryInstruction(dest=dest, src=src):
                _dest = dest.label
                _src = src.label
                _src2 = None
            case MathInstruction( dest=dest, src1=src1, src2=src2):
                _dest = dest.label
                _src = src1.label
                _src2 = src2.label
            case _:
                raise NotImplementedError()

        if _src in reg.register_allocation_table:
            val1 = None
            rs1 = _src
        else:
            val1 = reg.get_register_value(_src)
            rs1 = None

        if _src2 and _src2 in reg.register_allocation_table:
            _val2 = None
            rs2 = _src2
        elif _src2:
            _val2 = reg.get_register_value(_src2)
            rs2 = None
        return replace(src_rs, op=_op, val1=val1, val2=val2, rs1=rs1, rs2=rs2)


def issue(p: Processor) -> IssueAction | None:
    if p.instruction_queue:
        ins = p.instruction_queue[0]
        for ex_unit in p.execution_units:
            if ins.op in ex_unit.op_times.keys():
                for name, rs in ex_unit.reservation_stations.items():
                    if not rs.op:
                        return IssueAction(p, ex_unit, name)
    return None


