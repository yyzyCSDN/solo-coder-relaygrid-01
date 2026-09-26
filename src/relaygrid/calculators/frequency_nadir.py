from __future__ import annotations

def frequency_nadir_hz(nominal_hz: float, imbalance_kw: float, inertia_kw_s_per_hz: float) -> float:
    return nominal_hz - abs(imbalance_kw) / max(1.0, inertia_kw_s_per_hz)

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
