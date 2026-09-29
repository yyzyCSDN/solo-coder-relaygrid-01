from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

class SwitchState(str, Enum):
    OPEN = "open"
    CLOSED = "closed"

@dataclass(frozen=True)
class Bus:
    bus_id: str
    kv_ll: float
    phase_mask: str = "ABC"
    criticality: int = 0
    customers: int = 0
    demand_kw: float = 0.0
    demand_kvar: float = 0.0

@dataclass(frozen=True)
class Branch:
    branch_id: str
    source: str
    target: str
    r_ohm: float
    x_ohm: float
    ampacity_a: float
    switchable: bool = False
    normally_closed: bool = True

@dataclass(frozen=True)
class TelemetrySample:
    point_id: str
    timestamp_s: float
    sequence: int
    value: float
    quality: str = "good"

@dataclass
class FeederSnapshot:
    buses: dict[str, Bus] = field(default_factory=dict)
    branches: dict[str, Branch] = field(default_factory=dict)
    switch_state: dict[str, SwitchState] = field(default_factory=dict)

    def is_closed(self, branch: Branch) -> bool:
        """Resolve the energized state of a branch.

        Real-time telemetry in ``switch_state`` always wins. When no live
        indication is present the static model's normal position is used, so
        a normally-open tie is treated as open instead of closed.
        """
        if not branch.switchable:
            return True
        state = self.switch_state.get(branch.branch_id)
        if state is None:
            return branch.normally_closed
        return state == SwitchState.CLOSED

    def closed_branches(self) -> Iterable[Branch]:
        for br in self.branches.values():
            if self.is_closed(br):
                yield br

    def copy(self) -> "FeederSnapshot":
        return FeederSnapshot(dict(self.buses), dict(self.branches), dict(self.switch_state))
