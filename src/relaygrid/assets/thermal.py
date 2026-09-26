from __future__ import annotations
import math

def hottest_spot_step(previous_c: float, ambient_c: float, load_pu: float, dt_minutes: float, rated_rise_c: float=55.0, tau_minutes: float=180.0) -> float:
    if dt_minutes < 0 or tau_minutes <= 0 or load_pu < 0: raise ValueError("invalid thermal input")
    ultimate=ambient_c+rated_rise_c*(load_pu**1.6)
    alpha=1.0-math.exp(-dt_minutes/tau_minutes)
    return previous_c+(ultimate-previous_c)*alpha

def aging_acceleration(hotspot_c: float) -> float:
    return math.exp(15000.0/383.0-15000.0/(hotspot_c+273.0))

def equivalent_aging_hours(temperatures_c: list[float], step_minutes: float) -> float:
    if step_minutes < 0: raise ValueError("step must be nonnegative")
    return sum(aging_acceleration(t)*step_minutes/60.0 for t in temperatures_c)

def emergency_headroom(current_c: float, limit_c: float=140.0) -> float:
    return max(0.0,limit_c-current_c)
