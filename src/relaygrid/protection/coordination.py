from __future__ import annotations
import math

def secondary_current(primary_a: float, ct_primary: float, ct_secondary: float=5.0) -> float:
    if min(primary_a, ct_primary, ct_secondary) <= 0:
        raise ValueError("currents and CT ratings must be positive")
    return primary_a * ct_secondary / ct_primary

def iec_inverse_time(current_a: float, pickup_a: float, tms: float, curve: str="standard") -> float:
    if current_a <= pickup_a:
        return math.inf
    if pickup_a <= 0 or tms <= 0:
        raise ValueError("pickup and TMS must be positive")
    curves={"standard":(0.14,0.02),"very":(13.5,1.0),"extreme":(80.0,2.0)}
    if curve not in curves: raise ValueError(curve)
    k,alpha=curves[curve]
    multiple=current_a/pickup_a
    return tms*k/(multiple**alpha-1.0)

def relay_operating_time(primary_fault_a: float, ct_primary: float, pickup_secondary_a: float, tms: float, curve: str="standard") -> float:
    sec=secondary_current(primary_fault_a, ct_primary)
    return iec_inverse_time(sec, pickup_secondary_a, tms, curve)

def coordination_margin(upstream_s: float, downstream_s: float, breaker_s: float=0.08) -> float:
    if any(x < 0 for x in (upstream_s,downstream_s,breaker_s)):
        raise ValueError("times cannot be negative")
    return upstream_s-downstream_s-breaker_s

def coordinated(upstream_s: float, downstream_s: float, required_margin_s: float=0.25, breaker_s: float=0.08) -> bool:
    return coordination_margin(upstream_s,downstream_s,breaker_s) >= required_margin_s
