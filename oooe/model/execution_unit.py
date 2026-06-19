from dataclasses import dataclass
from typing import Optional

from oooe.model.reservation_station import ReservationStation


@dataclass
class ExecutionUnit:
    op_times: dict[str, int]

    reservation_stations: dict[str, ReservationStation]
    executing_rs: Optional[str] = None
    cycles_remaining: Optional[int] = None
