from dataclasses import dataclass, field

from oooe.model.instruction import Instruction


@dataclass
class Program:
    instructions: list[Instruction] = field(default_factory=list)
    label_address_map: dict[str, int] = field(default_factory=dict)
