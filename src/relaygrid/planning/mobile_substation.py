from __future__ import annotations
def deployment_score(outage_mva: float,duration_h: float,travel_h: float):
    a=outage_mva; b=duration_h; c=travel_h
    return max(0.0,a)*max(0.0,b)/max(0.25,c)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
