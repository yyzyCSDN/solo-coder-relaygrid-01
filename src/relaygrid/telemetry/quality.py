from __future__ import annotations
from relaygrid.models import TelemetrySample

def accept_sample(current: TelemetrySample|None, incoming: TelemetrySample) -> bool:
    if incoming.quality not in {"good","suspect"}: return False
    if current is None: return True
    if incoming.sequence > current.sequence: return True
    if incoming.sequence < current.sequence: return False
    return incoming.timestamp_s > current.timestamp_s

def newest_valid(samples: list[TelemetrySample]) -> TelemetrySample|None:
    cur=None
    for s in samples:
        if accept_sample(cur,s): cur=s
    return cur

def stale(sample: TelemetrySample|None, now_s: float, max_age_s: float) -> bool:
    if max_age_s < 0: raise ValueError("max age cannot be negative")
    if sample is None: return True
    return now_s-sample.timestamp_s > max_age_s

def quality_score(sample: TelemetrySample|None, now_s: float, max_age_s: float) -> float:
    if sample is None or sample.quality not in {"good","suspect"}: return 0.0
    age=max(0.0,now_s-sample.timestamp_s)
    freshness=max(0.0,1.0-age/max_age_s) if max_age_s else float(age==0)
    base=1.0 if sample.quality=="good" else 0.6
    return base*freshness
