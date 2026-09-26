from __future__ import annotations
from dataclasses import dataclass, field
@dataclass(frozen=True)
class Event:
    ts: float
    kind: str
    entity: str
    detail: str
@dataclass
class Logbook:
    events: list[Event]=field(default_factory=list)
    def append(self,event: Event):
        if self.events and event.ts < self.events[-1].ts: raise ValueError("events must be append-ordered")
        self.events.append(event)
    def between(self,start: float,end: float): return [e for e in self.events if start<=e.ts<=end]
    def by_entity(self,entity: str): return [e for e in self.events if e.entity==entity]
