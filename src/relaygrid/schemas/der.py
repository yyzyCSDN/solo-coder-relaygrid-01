from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class DERUnit:
    identifier: str
    status: str = "active"
    priority: int = 0
    attributes: tuple[tuple[str,Any], ...] = ()

    def get(self,key: str,default=None):
        for k,v in self.attributes:
            if k==key: return v
        return default

@dataclass(frozen=True)
class IslandPlan:
    identifier: str
    status: str = "active"
    priority: int = 1
    attributes: tuple[tuple[str,Any], ...] = ()

    def get(self,key: str,default=None):
        for k,v in self.attributes:
            if k==key: return v
        return default

@dataclass(frozen=True)
class ReserveRequirement:
    identifier: str
    status: str = "active"
    priority: int = 2
    attributes: tuple[tuple[str,Any], ...] = ()

    def get(self,key: str,default=None):
        for k,v in self.attributes:
            if k==key: return v
        return default

@dataclass(frozen=True)
class BlackStartStep:
    identifier: str
    status: str = "active"
    priority: int = 3
    attributes: tuple[tuple[str,Any], ...] = ()

    def get(self,key: str,default=None):
        for k,v in self.attributes:
            if k==key: return v
        return default

def active(records):
    return [r for r in records if r.status=="active"]

def by_priority(records):
    return sorted(records,key=lambda r:(-r.priority,r.identifier))
