from __future__ import annotations

def cold_load_kw(base_kw: float, outage_h: float, diversity: float) -> float:
    return base_kw * (1.0 + max(0.0, outage_h) ** 0.5 * diversity)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
