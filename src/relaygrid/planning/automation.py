from __future__ import annotations
def automation_score(operations_year: float,minutes_saved: float,cost: float):
    a=operations_year; b=minutes_saved; c=cost
    return max(0.0,a)*max(0.0,b)/max(1.0,c)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
