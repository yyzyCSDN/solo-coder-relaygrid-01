from __future__ import annotations
from statistics import mean

def weather_adjusted(base_kw: float, temperature_c: float, heating_balance_c: float=16.0, cooling_balance_c: float=22.0, heat_slope: float=0.025, cool_slope: float=0.035) -> float:
    if base_kw < 0: raise ValueError("base demand cannot be negative")
    factor=1.0
    if temperature_c < heating_balance_c: factor += (heating_balance_c-temperature_c)*heat_slope
    if temperature_c > cooling_balance_c: factor += (temperature_c-cooling_balance_c)*cool_slope
    return base_kw*factor

def moving_profile(samples: list[float], window: int=4) -> list[float]:
    if window <= 0: raise ValueError("window must be positive")
    out=[]
    for i in range(len(samples)):
        lo=max(0,i-window+1); out.append(mean(samples[lo:i+1]))
    return out

def diversity_peak(loads_kw: list[float], diversity_factor: float) -> float:
    if not 0 < diversity_factor <= 1: raise ValueError("diversity factor out of range")
    return sum(max(0.0,x) for x in loads_kw)*diversity_factor

def ramp_limit(profile: list[float], max_ramp_kw: float) -> list[float]:
    if max_ramp_kw < 0: raise ValueError("negative ramp")
    if not profile: return []
    out=[profile[0]]
    for value in profile[1:]: out.append(max(out[-1]-max_ramp_kw,min(out[-1]+max_ramp_kw,value)))
    return out
