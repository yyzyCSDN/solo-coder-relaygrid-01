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

    def resolved_switch_state(self, branch: Branch) -> SwitchState:
        """Resolve the effective state of a switchable branch.

        Real-time telemetry (``switch_state``) always wins. When the static
        model carries no telemetry, fall back to the designed normal state:
        a normally-open tie must resolve OPEN, never default to CLOSED.
        """
        if branch.branch_id in self.switch_state:
            return self.switch_state[branch.branch_id]
        return SwitchState.CLOSED if branch.normally_closed else SwitchState.OPEN

    def closed_branches(self) -> Iterable[Branch]:
        for br in self.branches.values():
            if not br.switchable:
                yield br
            elif self.resolved_switch_state(br) == SwitchState.CLOSED:
                yield br

    def copy(self) -> "FeederSnapshot":
        return FeederSnapshot(dict(self.buses), dict(self.branches), dict(self.switch_state))
