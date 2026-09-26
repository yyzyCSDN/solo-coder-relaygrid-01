from __future__ import annotations

def derated_ampacity(base_ampacity_a: float, soil_factor: float, grouping_factor: float, temperature_factor: float) -> float:
    return base_ampacity_a * soil_factor * grouping_factor * temperature_factor

def bounded(value: float,low: float,high: float) -> float:
    if high<low: raise ValueError("invalid bounds")
    return max(low,min(high,value))
