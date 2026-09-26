from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class Evidence:
    group_id: str
    timestamp_min: float
    state: str
    source: str
    confidence: float

@dataclass(frozen=True)
class Interval:
    group_id: str
    start_min: float
    end_min: float|None
    opening_source: str
    closing_source: str|None

SOURCE_WEIGHT={"breaker":1.0,"scada":.95,"ami":.85,"customer":.55,"prediction":.35}


def evidence_score(e:Evidence): return max(0.0,min(1.0,e.confidence))*SOURCE_WEIGHT.get(e.source,.2)


def reconcile(evidence:list[Evidence],minimum_score:float=.4):
    by=defaultdict(list)
    for e in evidence:
        if e.state not in {"out","restored"}: continue
        if evidence_score(e)>=minimum_score: by[e.group_id].append(e)
    result=[]
    for group,items in by.items():
        items=sorted(items,key=lambda e:(e.timestamp_min,-evidence_score(e)))
        open_ev=None
        for e in items:
            if e.state=="out" and open_ev is None: open_ev=e
            elif e.state=="restored" and open_ev is not None and e.timestamp_min>=open_ev.timestamp_min:
                result.append(Interval(group,open_ev.timestamp_min,e.timestamp_min,open_ev.source,e.source)); open_ev=None
        if open_ev is not None: result.append(Interval(group,open_ev.timestamp_min,None,open_ev.source,None))
    return sorted(result,key=lambda i:(i.group_id,i.start_min))


def closed_minutes(intervals:list[Interval],now_min:float):
    total=0.0
    for i in intervals:
        end=now_min if i.end_min is None else i.end_min
        total+=max(0.0,end-i.start_min)
    return total
