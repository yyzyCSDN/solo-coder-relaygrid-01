from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Section:
    section_id: str
    customers: int
    failure_rate_per_year: float
    repair_hours: float
    switching_hours: float=0.0
    has_remote_switch: bool=False

def expected_customer_hours(sections: list[Section]) -> float:
    total=0.0
    downstream=0
    for s in reversed(sections):
        downstream+=s.customers
        isolation=s.switching_hours*(0.25 if s.has_remote_switch else 1.0)
        total+=s.failure_rate_per_year*(s.customers*s.repair_hours + max(0,downstream-s.customers)*isolation)
    return total

def rank_automation_candidates(sections: list[Section], remote_switch_cost: float):
    base=expected_customer_hours(sections)
    out=[]
    for i,s in enumerate(sections):
        if s.has_remote_switch: continue
        trial=list(sections); trial[i]=Section(s.section_id,s.customers,s.failure_rate_per_year,s.repair_hours,s.switching_hours,True)
        saved=max(0.0,base-expected_customer_hours(trial))
        score=saved/remote_switch_cost if remote_switch_cost>0 else float('inf')
        out.append((score,saved,s.section_id))
    return sorted(out,reverse=True)
