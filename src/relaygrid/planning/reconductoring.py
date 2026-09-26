from __future__ import annotations

def voltage_benefit_kw(old_r: float,new_r: float,current_a: float,voltage_kv: float):
    if voltage_kv<=0: raise ValueError("voltage")
    saved_loss_kw=3*current_a*current_a*max(0.0,old_r-new_r)/1000
    return saved_loss_kw

def rank_projects(projects):
    scored=[]
    for pid,cost,saidi_saved,loss_saved in projects:
        benefit=saidi_saved*1000+loss_saved*120
        scored.append((benefit/cost if cost>0 else float('inf'),pid))
    return sorted(scored,reverse=True)
