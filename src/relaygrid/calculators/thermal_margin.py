from __future__ import annotations

def thermal_margin_a(ampacity_a: float, current_a: float) -> float:
    return ampacity_a - current_a

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
