from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CustomerInterruption:
    event_id: str
    customers: int
    duration_min: float
    momentary: bool=False


def saidi(events:list[CustomerInterruption],customers_served:int):
    if customers_served<=0: raise ValueError("customers served")
    minutes=sum(e.customers*e.duration_min for e in events if not e.momentary)
    return minutes/customers_served


def saifi(events:list[CustomerInterruption],customers_served:int):
    if customers_served<=0: raise ValueError("customers served")
    interruptions=sum(e.customers for e in events if not e.momentary)
    return interruptions/customers_served


def maifi(events:list[CustomerInterruption],customers_served:int):
    if customers_served<=0: raise ValueError("customers served")
    moments=sum(e.customers for e in events if e.momentary)
    return moments/customers_served


def caidi(events:list[CustomerInterruption],customers_served:int):
    f=saifi(events,customers_served)
    return 0.0 if f==0 else saidi(events,customers_served)/f


def cemi(events_by_customer:dict[str,int],threshold:int=3):
    if not events_by_customer:return 0.0
    affected=sum(1 for n in events_by_customer.values() if n>=threshold)
    return affected/len(events_by_customer)


def normalize_to_hours(value_minutes:float): return value_minutes/60
