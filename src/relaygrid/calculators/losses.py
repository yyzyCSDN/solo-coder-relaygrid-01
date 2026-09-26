from __future__ import annotations

def three_phase_loss_kw(current_a: float, r_ohm: float) -> float:
    return 3.0 * current_a * current_a * r_ohm / 1000.0

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
