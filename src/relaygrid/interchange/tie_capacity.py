from __future__ import annotations

def transferable_kw(tie_ampacity_a: float,kv_ll: float,power_factor: float,source_headroom_kw: float,receiving_need_kw: float):
    thermal=1.7320508075688772*kv_ll*tie_ampacity_a*power_factor
    return max(0.0,min(thermal,source_headroom_kw,receiving_need_kw))

def rank_ties(ties):
    return sorted(ties,key=lambda x:(-x[1],x[0]))
