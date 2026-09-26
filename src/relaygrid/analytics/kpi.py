from __future__ import annotations

def restoration_curve(points: list[tuple[float,int]],total_customers: int):
    if total_customers<=0: raise ValueError("total customers")
    return [(t,min(1.0,max(0.0,restored/total_customers))) for t,restored in sorted(points)]

def auc(curve: list[tuple[float,float]]):
    total=0.0
    for (t1,y1),(t2,y2) in zip(curve,curve[1:]): total+=(t2-t1)*(y1+y2)/2
    return total
