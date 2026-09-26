from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StorageState:
    energy_kwh: float
    capacity_kwh: float
    min_soc: float=0.1
    max_soc: float=0.95

def dispatch(state: StorageState, requested_kw: float, duration_h: float, charge_eff: float=0.95, discharge_eff: float=0.95):
    if state.capacity_kwh <= 0 or duration_h < 0: raise ValueError("invalid storage state")
    if not 0 < charge_eff <= 1 or not 0 < discharge_eff <= 1: raise ValueError("invalid efficiency")
    min_e=state.capacity_kwh*state.min_soc; max_e=state.capacity_kwh*state.max_soc
    e=min(max(state.energy_kwh,min_e),max_e)
    if requested_kw >= 0:
        max_deliverable=max(0.0,(e-min_e)*discharge_eff/duration_h) if duration_h else 0.0
        actual=min(requested_kw,max_deliverable)
        new_e=e-actual*duration_h/discharge_eff
    else:
        charge_kw=-requested_kw
        max_absorb=max(0.0,(max_e-e)/(charge_eff*duration_h)) if duration_h else 0.0
        actual=-min(charge_kw,max_absorb)
        new_e=e+(-actual)*duration_h*charge_eff
    return actual,StorageState(new_e,state.capacity_kwh,state.min_soc,state.max_soc)

def soc(state: StorageState) -> float:
    return state.energy_kwh/state.capacity_kwh
