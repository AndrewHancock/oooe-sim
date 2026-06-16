from dataclasses import dataclass
from typing import Optional


@dataclass
class ReservationStation:
    name: str
    op: Optional[str] = None
    val1: Optional[int] = None
    val2: Optional[str] = None
    rs1: Optional[str] = None
    rs2: Optional[str] = None

    def clear(self):
        self.op = None
        self.val1 = None
        self.val2 = None
        self.rs1 = None
        self.rs2 = None
