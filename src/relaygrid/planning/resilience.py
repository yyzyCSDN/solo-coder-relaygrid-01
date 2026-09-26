from __future__ import annotations
def resilience_score(critical_kw: float,backup_hours: float,isolation_minutes: float):
    a=critical_kw; b=backup_hours; c=isolation_minutes
    return max(0.0,a)*max(0.0,b)/(1+max(0.0,c))

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
