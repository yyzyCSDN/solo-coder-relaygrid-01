from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SourceCapacity:
    source_id: str
    normal_kw: float
    current_kw: float
    emergency_kw: float

@dataclass(frozen=True)
class TieCandidate:
    tie_id: str
    source_id: str
    load_kw: float
    tie_limit_kw: float
    estimated_low_voltage_pu: float
    risk_score: float

@dataclass(frozen=True)
class TransferDecision:
    tie_id: str
    accepted: bool
    transferable_kw: float
    reasons: tuple[str,...]


def evaluate_candidate(candidate:TieCandidate,source:SourceCapacity,min_voltage_pu:float=.95,max_risk:float=.7):
    reasons=[]
    headroom=max(0.0,source.emergency_kw-source.current_kw)
    transferable=min(candidate.load_kw,candidate.tie_limit_kw,headroom)
    if candidate.source_id!=source.source_id: reasons.append("source_mismatch")
    if transferable+1e-9<candidate.load_kw: reasons.append("insufficient_capacity")
    if candidate.estimated_low_voltage_pu<min_voltage_pu: reasons.append("low_voltage")
    if candidate.risk_score>max_risk: reasons.append("risk_limit")
    return TransferDecision(candidate.tie_id,not reasons,transferable,tuple(reasons))


def choose_backfeeds(candidates:list[TieCandidate],sources:dict[str,SourceCapacity],max_count:int=3):
    scored=[]
    for c in candidates:
        s=sources.get(c.source_id)
        if s is None: continue
        d=evaluate_candidate(c,s)
        benefit=d.transferable_kw*(1-c.risk_score)
        scored.append((not d.accepted,-benefit,c.tie_id,d))
    return [item[-1] for item in sorted(scored)[:max_count]]


def apply_transfers(decisions:list[TransferDecision],sources:dict[str,SourceCapacity],candidates:dict[str,TieCandidate]):
    usage={k:v.current_kw for k,v in sources.items()}
    applied=[]
    for d in decisions:
        if not d.accepted: continue
        c=candidates[d.tie_id]; s=sources[c.source_id]
        remaining=max(0.0,s.emergency_kw-usage[c.source_id])
        take=min(d.transferable_kw,remaining)
        if take<=0: continue
        usage[c.source_id]+=take; applied.append((d.tie_id,take))
    return applied,usage
