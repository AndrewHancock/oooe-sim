from dataclasses import dataclass, field

from oooe.model import reservation_station
from oooe.model.execution_unit import ExecutionUnit
from oooe.model.instruction import Instruction
from oooe.model.registers import RegisterFile
from oooe.model.reservation_station import ReservationStation


@dataclass
class Processor:
    execution_units: list[ExecutionUnit]
    instruction_queue: list[Instruction] = field(default_factory=list)
    registers :RegisterFile = field(default_factory=RegisterFile)

def get_processor(instructions: list[Instruction]) -> Processor:
    load_rs = [ReservationStation(name='LD' + str(i + 1)) for i in  range(0, 2)]
    add_rs = [ReservationStation(name='AD' + str(i + 1)) for i in range(0, 3)]
    mul_rs = [ReservationStation(name='ML' + str(i + 1)) for i in range(0, 2)]

    execution_units = [
        ExecutionUnit(op_times={'L.D' : 2}, reservation_stations={rs.name: rs for rs in load_rs}),
        ExecutionUnit(op_times={'SUB.D': 2, 'ADD.D': 2}, reservation_stations={rs.name: rs for rs in add_rs}),
        ExecutionUnit(op_times={'MUL.D': 10, 'DIV.D': 40}, reservation_stations={rs.name: rs for rs in mul_rs})
    ]

    return Processor(execution_units=execution_units, instruction_queue=instructions)