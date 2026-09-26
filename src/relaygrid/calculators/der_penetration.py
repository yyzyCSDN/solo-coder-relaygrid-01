from __future__ import annotations

def penetration_pct(der_kw: float, peak_load_kw: float) -> float:
    return 100.0 * der_kw / max(1e-9, peak_load_kw)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
