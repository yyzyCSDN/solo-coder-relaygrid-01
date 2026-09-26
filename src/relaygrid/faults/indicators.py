from __future__ import annotations

def infer_fault_zone(indicators: list[tuple[str,int,bool]], breaker_tripped: bool):
    if not breaker_tripped: return []
    asserted=[(order,name) for name,order,state in indicators if state]
    clear=[(order,name) for name,order,state in indicators if not state]
    if not asserted: return []
    farthest=max(asserted)[0]
    downstream=[name for order,name in sorted(clear) if order>farthest]
    return downstream[:1] if downstream else [max(asserted)[1]]

def confidence(asserted_count: int,total_count: int,telemetry_quality: float):
    if total_count<=0: return 0.0
    return min(1.0,max(0.0,asserted_count/total_count)*max(0.0,min(1.0,telemetry_quality)))
