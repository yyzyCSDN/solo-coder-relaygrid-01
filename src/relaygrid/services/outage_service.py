from __future__ import annotations
from collections import defaultdict
from relaygrid.outage.metrics import merge_intervals, interruption_minutes

class OutageService:
    def __init__(self): self._events=[]
    def add(self,customer_group: str,customers: int,start_min: float,end_min: float):
        if customers<0 or end_min<start_min: raise ValueError("invalid outage")
        self._events.append((customer_group,customers,start_min,end_min))
    def customer_minutes(self):
        grouped=defaultdict(list); counts={}
        for group,customers,start,end in self._events:
            grouped[group].append((start,end)); counts[group]=customers
        return sum(counts[g]*interruption_minutes(iv) for g,iv in grouped.items())
    def group_summaries(self):
        grouped=defaultdict(list); counts={}
        for group,customers,start,end in self._events:
            grouped[group].append((start,end)); counts[group]=customers
        return {g:{"customers":counts[g],"intervals":merge_intervals(iv),"minutes":interruption_minutes(iv)} for g,iv in grouped.items()}
