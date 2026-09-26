from __future__ import annotations

def prioritize_incidents(incidents):
    def key(x):
        iid,customers,critical,hazard,age_min=x
        score=customers+critical*500+hazard*800+age_min*2
        return (-score,iid)
    return [x for x in sorted(incidents,key=key)]

def sla_breached(opened_min: float,now_min: float,sla_min: float): return now_min-opened_min>sla_min
