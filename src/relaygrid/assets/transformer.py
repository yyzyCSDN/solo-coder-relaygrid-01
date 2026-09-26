from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class TransformerState:
    top_oil_c: float
    hotspot_c: float
    loss_of_life_hours: float

@dataclass(frozen=True)
class TransformerRating:
    kva: float
    top_oil_rise_c: float=55.0
    hotspot_gradient_c: float=30.0
    oil_tau_h: float=3.0
    winding_tau_h: float=.25


def _approach(previous:float,ultimate:float,dt_h:float,tau_h:float): return ultimate-(ultimate-previous)*math.exp(-dt_h/tau_h)


def step(state:TransformerState,rating:TransformerRating,ambient_c:float,load_kva:float,dt_h:float):
    if dt_h<0 or rating.kva<=0: raise ValueError("invalid transformer step")
    k=max(0.0,load_kva/rating.kva)
    ultimate_oil=ambient_c+rating.top_oil_rise_c*(k**1.6)
    new_oil=_approach(state.top_oil_c,ultimate_oil,dt_h,rating.oil_tau_h)
    ultimate_hot=new_oil+rating.hotspot_gradient_c*(k**1.8)
    new_hot=_approach(state.hotspot_c,ultimate_hot,dt_h,rating.winding_tau_h)
    aging=math.exp(15000/383-15000/(new_hot+273))*dt_h
    return TransformerState(new_oil,new_hot,state.loss_of_life_hours+aging)


def emergency_duration_h(state:TransformerState,limit_c:float=140.0,max_aging_h:float=24.0):
    thermal=max(0.0,(limit_c-state.hotspot_c)/20)
    aging=max(0.0,max_aging_h-state.loss_of_life_hours)
    return min(thermal,aging)


def loading_class(load_kva:float,rating:TransformerRating):
    pu=load_kva/rating.kva
    if pu<=.8:return "normal"
    if pu<=1:return "high_normal"
    if pu<=1.2:return "emergency"
    return "overload"
