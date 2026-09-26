from __future__ import annotations

def allocate_ev(chargers: list[tuple[str,float,float]], feeder_headroom_kw: float):
    ordered=sorted(chargers,key=lambda x:(x[2],x[0]))
    out={}; remaining=max(0.0,feeder_headroom_kw)
    for cid,max_kw,deadline_h in ordered:
        take=min(max_kw,remaining); out[cid]=take; remaining-=take
    return out

def coincident_peak_kw(charger_kw: list[float], coincidence: float=0.65):
    if not 0<=coincidence<=1: raise ValueError("coincidence out of range")
    return sum(max(0.0,x) for x in charger_kw)*coincidence
