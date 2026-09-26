from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FlexOffer:
    offer_id: str
    kw: float
    price_per_kwh: float
    duration_h: float
    must_run: bool=False

def clear_offers(offers: list[FlexOffer], required_kw: float):
    chosen=[]; remaining=max(0.0,required_kw)
    for o in sorted(offers,key=lambda x:(not x.must_run,x.price_per_kwh,x.offer_id)):
        if remaining<=0 and not o.must_run: continue
        take=min(o.kw,remaining) if not o.must_run else o.kw
        if take>0: chosen.append((o.offer_id,take,take*o.duration_h*o.price_per_kwh)); remaining=max(0.0,remaining-take)
    return chosen,remaining
