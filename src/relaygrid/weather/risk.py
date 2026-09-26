from __future__ import annotations
import math

def wind_failure_probability(wind_mps: float, midpoint: float=30.0, slope: float=0.25):
    x=slope*(wind_mps-midpoint); return 1.0/(1.0+math.exp(-x))

def icing_index(precip_mm: float, temp_c: float, wind_mps: float):
    if precip_mm<=0 or temp_c>1.0: return 0.0
    thermal=max(0.0,1.0-abs(temp_c+1.5)/4.0)
    return precip_mm*thermal*(1+min(wind_mps,20)/20)

def patrol_priority(probability: float, customers: int, critical_sites: int):
    return max(0.0,min(1.0,probability))*(customers+250*critical_sites)
