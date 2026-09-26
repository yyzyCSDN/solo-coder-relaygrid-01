from __future__ import annotations

def unbalance_pct(avg_v: float, va: float, vb: float, vc: float) -> float:
    return 0.0 if avg_v == 0 else 100.0 * max(abs(va-avg_v),abs(vb-avg_v),abs(vc-avg_v)) / avg_v

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
