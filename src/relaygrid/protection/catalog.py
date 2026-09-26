from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ProtectionDevice:
    code: str
    rating_a: float
    instantaneous_multiple: float
    interrupt_ka: float
CATALOG={
    "FUSE_40": ProtectionDevice("FUSE_40",40,1.8,12),
    "FUSE_65": ProtectionDevice("FUSE_65",65,1.7,15),
    "REC_200": ProtectionDevice("REC_200",200,1.2,8),
    "REL_600": ProtectionDevice("REL_600",600,1.1,5),
}
def interrupting_ok(code: str,fault_ka: float): return fault_ka<=CATALOG[code].interrupt_ka
def pickup_primary(code: str):
    d=CATALOG[code]; return d.rating_a*d.instantaneous_multiple
