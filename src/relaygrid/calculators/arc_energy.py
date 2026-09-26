from __future__ import annotations

def incident_energy_proxy(fault_ka: float, clearing_s: float, gap_factor: float) -> float:
    return fault_ka * fault_ka * clearing_s * max(0.1, gap_factor)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
