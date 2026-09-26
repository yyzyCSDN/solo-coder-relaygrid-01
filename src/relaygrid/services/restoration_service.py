from __future__ import annotations
from dataclasses import dataclass
from relaygrid.restoration.sequence import CandidateStep, rank_steps
from relaygrid.loads.priority import LoadBlock, select_to_serve
from relaygrid.der.islanding import Resource, assess_island

@dataclass(frozen=True)
class RestorationRequest:
    capacity_kw: float
    load_blocks: tuple[LoadBlock,...]
    switching_candidates: tuple[CandidateStep,...]
    resources: tuple[Resource,...]=()

class RestorationService:
    def plan(self,request: RestorationRequest):
        served=select_to_serve(list(request.load_blocks),request.capacity_kw)
        ranked=rank_steps(list(request.switching_candidates))
        island_load=sum(served.values())
        island=assess_island(island_load,list(request.resources)) if request.resources else None
        return {"served":served,"switching":[s.branch_id for s in ranked],"island":island}
    def unserved_kw(self,request: RestorationRequest):
        plan=self.plan(request); demand=sum(max(0.0,b.kw*b.cold_load_multiplier) for b in request.load_blocks)
        return max(0.0,demand-sum(plan["served"].values()))
    def critical_served_ratio(self,request: RestorationRequest):
        plan=self.plan(request); critical=[b for b in request.load_blocks if b.priority>=8]
        denom=sum(b.kw*b.cold_load_multiplier for b in critical)
        if denom<=0: return 1.0
        num=sum(plan["served"].get(b.block_id,0.0) for b in critical)
        return num/denom
