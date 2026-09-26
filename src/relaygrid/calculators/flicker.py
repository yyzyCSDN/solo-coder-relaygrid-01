from __future__ import annotations

def flicker_index(delta_kw: float, short_circuit_mva: float) -> float:
    return abs(delta_kw) / max(1.0, short_circuit_mva * 1000.0)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
