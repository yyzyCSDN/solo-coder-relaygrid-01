from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class TransformerType:
    code: str
    kva: float
    no_load_loss_pct: float
    load_loss_pct: float
CATALOG={
    "TX_25": TransformerType("TX_25",25,2.1,1.4),
    "TX_50": TransformerType("TX_50",50,2.0,1.5),
    "TX_100": TransformerType("TX_100",100,1.9,1.6),
    "TX_500": TransformerType("TX_500",500,1.7,1.8),
}
def efficiency(code: str,load_pu: float,pf: float=0.95):
    t=CATALOG[code]; output=t.kva*load_pu*pf
    losses=t.kva*t.no_load_loss_pct/100+t.kva*t.load_loss_pct/100*load_pu*load_pu
    return output/(output+losses) if output+losses else 1.0
def overloaded(code: str,kva: float,emergency_factor: float=1.2): return kva>CATALOG[code].kva*emergency_factor
