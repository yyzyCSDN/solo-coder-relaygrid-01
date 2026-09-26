from __future__ import annotations
def priority_score(failure_rate: float,repair_hours: float,exposure: float):
    a=failure_rate; b=repair_hours; c=exposure
    return max(0.0,a)*max(0.0,b)*max(0.0,c)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
