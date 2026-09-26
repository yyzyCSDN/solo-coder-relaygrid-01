from __future__ import annotations

def power_factor(p_kw: float, q_kvar: float) -> float:
    return 0.0 if p_kw == 0 and q_kvar == 0 else abs(p_kw) / (p_kw*p_kw + q_kvar*q_kvar) ** 0.5

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
