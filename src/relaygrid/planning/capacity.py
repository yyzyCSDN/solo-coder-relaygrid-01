from __future__ import annotations

def n_minus_one_capacity(transformers_mva: list[float], peak_mva: float):
    if peak_mva<0 or any(x<=0 for x in transformers_mva): raise ValueError("invalid capacity")
    if len(transformers_mva)<2: return False,0.0
    remaining=sum(transformers_mva)-max(transformers_mva)
    return remaining>=peak_mva,remaining-peak_mva

def hosting_capacity(base_peak_kw: float, thermal_limit_kw: float, voltage_headroom_kw: float, reverse_limit_kw: float):
    if min(thermal_limit_kw,voltage_headroom_kw,reverse_limit_kw)<0: raise ValueError("negative limit")
    return max(0.0,min(thermal_limit_kw-base_peak_kw,voltage_headroom_kw,reverse_limit_kw))

def contingency_margin(limit: float, normal: float, contingency: float):
    return limit-max(normal,contingency)
