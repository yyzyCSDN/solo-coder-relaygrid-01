from __future__ import annotations

def neutral_current_a(ia: float, ib: float, ic: float) -> float:
    return abs(ia + ib + ic)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
