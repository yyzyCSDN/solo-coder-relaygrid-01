from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class MeterObservation:
    meter_id: str
    section_id: str
    timestamp_s: float
    voltage_v: float|None
    ping_ok: bool

@dataclass(frozen=True)
class SectionVerification:
    section_id: str
    state: str
    sample_count: int
    energized_ratio: float


def verify_sections(observations:list[MeterObservation],expected_energized:set[str],voltage_threshold:float=90.0):
    by=defaultdict(list)
    for o in observations: by[o.section_id].append(o)
    out=[]
    for section,obs in sorted(by.items()):
        energized=sum(1 for o in obs if o.ping_ok and o.voltage_v is not None and o.voltage_v>=voltage_threshold)
        ratio=energized/len(obs) if obs else 0.0
        expected=section in expected_energized
        if expected and ratio>=.8: state="confirmed"
        elif expected and ratio>=.2: state="partial"
        elif expected: state="contradictory"
        elif not expected and ratio>.2: state="unexpected_energized"
        else: state="confirmed_deenergized"
        out.append(SectionVerification(section,state,len(obs),ratio))
    return out


def contradictory(verifications:list[SectionVerification]):
    return [v for v in verifications if v.state in {"contradictory","unexpected_energized"}]
