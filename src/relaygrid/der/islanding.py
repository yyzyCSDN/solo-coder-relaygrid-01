from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Resource:
    resource_id: str
    available_kw: float
    min_kw: float=0.0
    grid_forming: bool=False
    spinning_reserve_kw: float=0.0

@dataclass(frozen=True)
class IslandAssessment:
    feasible: bool
    served_kw: float
    reserve_kw: float
    shortfall_kw: float
    has_grid_former: bool

def assess_island(load_kw: float, resources: list[Resource], reserve_fraction: float=0.10) -> IslandAssessment:
    if load_kw < 0 or reserve_fraction < 0: raise ValueError("invalid load or reserve")
    available=sum(max(0.0,r.available_kw) for r in resources)
    committed_reserve=sum(max(0.0,r.spinning_reserve_kw) for r in resources)
    required_reserve=load_kw*reserve_fraction
    usable=max(0.0,available-required_reserve)
    served=min(load_kw,usable)
    reserve=max(0.0,available-served)
    grid_former=any(r.grid_forming and r.available_kw>0 for r in resources)
    shortfall=max(0.0,load_kw-served)
    feasible=grid_former and shortfall <= 1e-9 and reserve+1e-9 >= required_reserve and reserve+1e-9 >= committed_reserve
    return IslandAssessment(feasible,served,reserve,shortfall,grid_former)

def black_start_order(resources: list[Resource]):
    formers=[r for r in resources if r.grid_forming and r.available_kw>0]
    followers=[r for r in resources if not r.grid_forming and r.available_kw>0]
    return [r.resource_id for r in sorted(formers,key=lambda x:(-x.available_kw,x.resource_id))] + [r.resource_id for r in sorted(followers,key=lambda x:(-x.available_kw,x.resource_id))]
