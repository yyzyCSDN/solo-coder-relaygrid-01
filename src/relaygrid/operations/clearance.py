from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class Clearance:
    clearance_id: str
    holder: str
    boundaries: frozenset[str]
    released: bool=False

def can_release(clearance: Clearance, confirmations: set[str]): return clearance.boundaries.issubset(confirmations) and not clearance.released

def overlapping(a: Clearance,b: Clearance): return bool(a.boundaries & b.boundaries) and not a.released and not b.released
