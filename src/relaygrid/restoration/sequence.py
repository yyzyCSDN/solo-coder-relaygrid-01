from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class CandidateStep:
    branch_id: str
    restored_kw: float
    restored_customers: int
    risk: float
    remote: bool

def rank_steps(steps: list[CandidateStep]):
    def score(s):
        benefit=s.restored_customers+0.2*s.restored_kw
        penalty=1+max(0.0,s.risk)*(1.5 if not s.remote else 1.0)
        return benefit/penalty
    return sorted(steps,key=lambda s:(-score(s),not s.remote,s.branch_id))

def sequence_until_target(steps: list[CandidateStep], target_customers: int):
    total=0; chosen=[]
    for s in rank_steps(steps):
        if total>=target_customers: break
        chosen.append(s); total+=s.restored_customers
    return chosen,total
