from __future__ import annotations
from dataclasses import dataclass, field
from relaygrid.models import TelemetrySample

@dataclass
class Cursor:
    point_id: str
    sequence: int
    timestamp_s: float

@dataclass
class Historian:
    rows: dict[str,list[TelemetrySample]]=field(default_factory=dict)

    def append(self,sample:TelemetrySample):
        bucket=self.rows.setdefault(sample.point_id,[])
        if bucket and sample.sequence<=bucket[-1].sequence: raise ValueError("historian sequence must increase")
        bucket.append(sample)

    def query(self,point_id:str,start_s:float,end_s:float):
        return [s for s in self.rows.get(point_id,[]) if start_s<=s.timestamp_s<=end_s]

    def after(self,cursor:Cursor,limit:int=1000):
        rows=[s for s in self.rows.get(cursor.point_id,[]) if s.sequence>cursor.sequence]
        return rows[:limit]

    def latest_cursor(self,point_id:str):
        rows=self.rows.get(point_id,[])
        if not rows: return Cursor(point_id,-1,float('-inf'))
        s=rows[-1]; return Cursor(point_id,s.sequence,s.timestamp_s)


def merge_live_and_recovery(live:list[TelemetrySample],recovered:list[TelemetrySample]):
    by_seq: dict[int,TelemetrySample]={}
    for sample in recovered+live:
        cur=by_seq.get(sample.sequence)
        if cur is None or sample.timestamp_s>cur.timestamp_s: by_seq[sample.sequence]=sample
    return [by_seq[k] for k in sorted(by_seq)]


def detect_gaps(samples:list[TelemetrySample]):
    if not samples: return []
    ordered=sorted(samples,key=lambda s:s.sequence); gaps=[]
    for a,b in zip(ordered,ordered[1:]):
        if b.sequence>a.sequence+1: gaps.append((a.sequence+1,b.sequence-1))
    return gaps
