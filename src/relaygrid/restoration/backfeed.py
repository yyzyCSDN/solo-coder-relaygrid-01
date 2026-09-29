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


def evaluate_candidate(candidate:TieCandidate,source:SourceCapacity,min_voltage_pu:float=.95,max_risk:float=.7,reserved_kw:float=0.0):
    reasons=[]
    # Headroom is net of capacity already reserved by candidates chosen earlier
    # for this same source, so two transfers can never each claim the full margin.
    headroom=max(0.0,source.emergency_kw-source.current_kw-reserved_kw)
    transferable=min(candidate.load_kw,candidate.tie_limit_kw,headroom)
    if candidate.source_id!=source.source_id: reasons.append("source_mismatch")
    if transferable+1e-9<candidate.load_kw: reasons.append("insufficient_capacity")
    if candidate.estimated_low_voltage_pu<min_voltage_pu: reasons.append("low_voltage")
    if candidate.risk_score>max_risk: reasons.append("risk_limit")
    return TransferDecision(candidate.tie_id,not reasons,transferable,tuple(reasons))


def choose_backfeeds(candidates:list[TieCandidate],sources:dict[str,SourceCapacity],max_count:int=3):
    # Rank by expected benefit (deterministic tie_id tiebreak), then walk the
    # ranking once, accumulating committed load per source. Every later
    # candidate for the same backup source is evaluated against what remains.
    ranked=sorted(
        candidates,
        key=lambda c:(-c.load_kw*(1-c.risk_score),c.tie_id),
    )
    reserved:dict[str,float]={}
    decisions=[]
    for c in ranked:
        s=sources.get(c.source_id)
        if s is None: continue
        d=evaluate_candidate(c,s,reserved_kw=reserved.get(c.source_id,0.0))
        if d.accepted:
            reserved[c.source_id]=reserved.get(c.source_id,0.0)+c.load_kw
        decisions.append(d)
        if len(decisions)>=max_count: break
    return decisions


def apply_transfers(decisions:list[TransferDecision],sources:dict[str,SourceCapacity],candidates:dict[str,TieCandidate]):
    # Settlement must match the preview exactly: every accepted decision is
    # served in full at its committed size, or none of them is applied.
    usage={k:v.current_kw for k,v in sources.items()}
    planned=[]
    for d in decisions:
        if not d.accepted: continue
        c=candidates[d.tie_id]; s=sources[c.source_id]
        remaining=s.emergency_kw-usage[c.source_id]
        if d.transferable_kw>remaining+1e-9:
            raise ValueError(
                f"tie {d.tie_id} rejected at execution: insufficient_capacity "
                f"on source {c.source_id} (need {d.transferable_kw:.3f} kW, "
                f"available {max(0.0,remaining):.3f} kW); no transfers applied"
            )
        usage[c.source_id]+=d.transferable_kw
        planned.append((c.source_id,d.tie_id,d.transferable_kw))
    applied=[]
    for source_id,tie_id,take in planned:
        applied.append((tie_id,take))
    return applied,usage
