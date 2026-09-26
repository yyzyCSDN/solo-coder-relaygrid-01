from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class LoadBlock:
    block_id: str
    kw: float
    priority: int
    min_service_kw: float=0.0
    cold_load_multiplier: float=1.0

def select_to_serve(blocks: list[LoadBlock], capacity_kw: float):
    remaining=max(0.0,capacity_kw); served={}
    ordered=sorted(blocks,key=lambda b:(-b.priority,b.block_id))
    for b in ordered:
        demand=max(0.0,b.kw*b.cold_load_multiplier)
        floor=min(demand,max(0.0,b.min_service_kw))
        if remaining+1e-9 < floor: served[b.block_id]=0.0; continue
        take=min(demand,remaining); served[b.block_id]=take; remaining-=take
    return served

def shed_order(blocks: list[LoadBlock]):
    return [b.block_id for b in sorted(blocks,key=lambda x:(x.priority,-x.kw,x.block_id))]
