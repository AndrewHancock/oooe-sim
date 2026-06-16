from dataclasses import dataclass
from typing import Optional

from oooe.model.reservation_station import ReservationStation


@dataclass
class ExecutionUnit:
    op_times: dict[str, int]

    reservation_stations: list[ReservationStation]

    cycles_to_complete: Optional[int] = None
    op: Optional[str] = None
    val1: Optional[int] = None
    val2: Optional[int] = None