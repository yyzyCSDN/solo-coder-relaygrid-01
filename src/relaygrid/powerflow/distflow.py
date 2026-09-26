from __future__ import annotations
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class SegmentFlow:
    segment_id: str
    sending_kv: float
    receiving_kv: float
    current_a: float
    loss_kw: float

def sweep_radial(nominal_kv_ll: float, demands: list[tuple[str,float,float,float,float]], tolerance: float=1e-6):
    voltage=nominal_kv_ll; flows=[]
    for segment_id,kw,kvar,r,x in demands:
        kva=math.hypot(kw,kvar); current=kva/(math.sqrt(3)*max(voltage,1e-9))
        loss_kw=3*(current**2)*r/1000
        drop=(r*kw+x*kvar)/(max(voltage,1e-9)*1000)
        recv=max(0.0,voltage-drop)
        flows.append(SegmentFlow(segment_id,voltage,recv,current,loss_kw)); voltage=recv
    return flows

def max_loading(flows: list[SegmentFlow], ampacities: dict[str,float]):
    ratios=[]
    for f in flows:
        rating=ampacities.get(f.segment_id)
        if rating and rating>0: ratios.append((f.current_a/rating,f.segment_id))
    return max(ratios,default=(0.0,None))
