from __future__ import annotations

def loading_pct(kva: float, rating_kva: float) -> float:
    return 100.0 * kva / max(1e-9, rating_kva)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
