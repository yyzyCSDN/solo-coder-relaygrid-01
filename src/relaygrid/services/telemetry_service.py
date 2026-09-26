from __future__ import annotations
from collections import defaultdict
from relaygrid.models import TelemetrySample
from relaygrid.telemetry.quality import newest_valid, stale

class TelemetryService:
    def __init__(self,max_age_s: float=120.0):
        self.max_age_s=max_age_s
        self._by_point: defaultdict[str,list[TelemetrySample]]=defaultdict(list)
    def ingest(self,sample: TelemetrySample): self._by_point[sample.point_id].append(sample)
    def latest(self,point_id: str): return newest_valid(self._by_point.get(point_id,[]))
    def snapshot(self,now_s: float):
        out={}
        for point_id in sorted(self._by_point):
            sample=self.latest(point_id)
            out[point_id]={"value":None if sample is None else sample.value,"stale":stale(sample,now_s,self.max_age_s),"quality":None if sample is None else sample.quality}
        return out
