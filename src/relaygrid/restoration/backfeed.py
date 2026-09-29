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

class TransferCapacityError(RuntimeError):
    """An accepted transfer cannot be delivered in full at execution time."""
    def __init__(self, tie_id: str, source_id: str, required_kw: float, available_kw: float):
        self.tie_id=tie_id
        self.source_id=source_id
        self.required_kw=required_kw
        self.available_kw=available_kw
        super().__init__(
            f"tie {tie_id} needs {required_kw:.3f} kW on source {source_id} "
            f"but only {available_kw:.3f} kW remains (insufficient_capacity)"
        )


def evaluate_candidate(candidate:TieCandidate,source:SourceCapacity,available_kw:float|None=None,min_voltage_pu:float=.95,max_risk:float=.7):
    reasons=[]
    headroom=max(0.0,source.emergency_kw-source.current_kw)
    if available_kw is None:
        available_kw=headroom
    transferable=min(candidate.load_kw,candidate.tie_limit_kw,max(0.0,available_kw))
    if candidate.source_id!=source.source_id: reasons.append("source_mismatch")
    if transferable+1e-9<candidate.load_kw: reasons.append("insufficient_capacity")
    if candidate.estimated_low_voltage_pu<min_voltage_pu: reasons.append("low_voltage")
    if candidate.risk_score>max_risk: reasons.append("risk_limit")
    return TransferDecision(candidate.tie_id,not reasons,transferable,tuple(reasons))


def choose_backfeeds(candidates:list[TieCandidate],sources:dict[str,SourceCapacity],max_count:int=3):
    # Rank candidates by benefit first; preview/rehearsal and execution both
    # consume this ordering so they cannot disagree.
    ranked=sorted(
        candidates,
        key=lambda c:(-min(c.load_kw,c.tie_limit_kw)*(1-c.risk_score),c.tie_id),
    )
    # Capacity is a shared, cumulative reserve per source: headroom left by
    # earlier accepted candidates is what later candidates may rely on.
    reserved={sid:s.current_kw for sid,s in sources.items()}
    accepted_count=0
    decisions=[]
    for c in ranked:
        s=sources.get(c.source_id)
        if s is None:
            reasons=("source_mismatch",)
            decisions.append(TransferDecision(c.tie_id,False,0.0,reasons))
            continue
        available=s.emergency_kw-reserved[c.source_id]
        d=evaluate_candidate(c,s,available)
        if d.accepted:
            if accepted_count>=max_count:
                d=TransferDecision(
                    c.tie_id,False,0.0,
                    d.reasons+("plan_count_limit",),
                )
            else:
                accepted_count+=1
                reserved[c.source_id]+=d.transferable_kw
        decisions.append(d)
    return decisions


def apply_transfers(decisions:list[TransferDecision],sources:dict[str,SourceCapacity],candidates:dict[str,TieCandidate]):
    accepted=[d for d in decisions if d.accepted]
    # Dry run first: any accepted plan that cannot land in full rejects the
    # whole batch instead of silently transferring part of the load.
    usage={k:v.current_kw for k,v in sources.items()}
    for d in accepted:
        c=candidates[d.tie_id]; s=sources[c.source_id]
        need=min(c.load_kw,c.tie_limit_kw)
        available=s.emergency_kw-usage[c.source_id]
        if need>available+1e-9:
            raise TransferCapacityError(d.tie_id,c.source_id,need,max(0.0,available))
        usage[c.source_id]+=need
    return [(d.tie_id,min(candidates[d.tie_id].load_kw,candidates[d.tie_id].tie_limit_kw)) for d in accepted],usage
