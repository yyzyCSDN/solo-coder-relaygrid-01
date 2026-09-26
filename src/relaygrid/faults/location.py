from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ImpedanceEstimate:
    distance_km: float
    fraction: float
    residual_ohm: float

def locate_reactance(measured_x_ohm: float, source_x_ohm: float, line_x_ohm_per_km: float, line_length_km: float) -> ImpedanceEstimate:
    if line_x_ohm_per_km <= 0 or line_length_km <= 0:
        raise ValueError("line parameters must be positive")
    raw=(measured_x_ohm-source_x_ohm)/line_x_ohm_per_km
    distance=min(line_length_km,max(0.0,raw))
    modeled=source_x_ohm+distance*line_x_ohm_per_km
    residual=measured_x_ohm-modeled
    return ImpedanceEstimate(distance,distance/line_length_km,residual)

def rank_sections(estimate: ImpedanceEstimate, sections: list[tuple[str,float,float]]):
    ranked=[]
    for name,start_km,end_km in sections:
        if end_km < start_km: raise ValueError("invalid section")
        if start_km <= estimate.distance_km <= end_km: gap=0.0
        else: gap=min(abs(estimate.distance_km-start_km),abs(estimate.distance_km-end_km))
        ranked.append((gap,name))
    return [name for _,name in sorted(ranked)]
