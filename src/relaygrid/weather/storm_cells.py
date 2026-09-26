from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class StormCell:
    cell_id: str
    center_lat: float
    center_lon: float
    radius_km: float
    wind_mps: float
    lightning_rate: float
    start_s: float
    end_s: float


def km_per_degree_lat(): return 111.195

def point_distance_km(lat1,lon1,lat2,lon2):
    y=(lat2-lat1)*km_per_degree_lat(); x=(lon2-lon1)*km_per_degree_lat()*math.cos(math.radians((lat1+lat2)/2))
    return math.hypot(x,y)


def contains(cell:StormCell,lat:float,lon:float,timestamp_s:float):
    return cell.start_s<=timestamp_s<=cell.end_s and point_distance_km(cell.center_lat,cell.center_lon,lat,lon)<=cell.radius_km


def severity(cell:StormCell):
    wind=max(0.0,(cell.wind_mps-15)/25)
    lightning=min(1.0,max(0.0,cell.lightning_rate)/60)
    return min(1.0,.7*wind+.3*lightning)


def affected_assets(cell:StormCell,assets:list[tuple[str,float,float]],timestamp_s:float):
    return [(aid,point_distance_km(cell.center_lat,cell.center_lon,lat,lon)) for aid,lat,lon in assets if contains(cell,lat,lon,timestamp_s)]


def merge_cells(cells:list[StormCell],overlap_ratio:float=.5):
    groups: list[list[StormCell]]=[]
    for cell in sorted(cells,key=lambda c:c.start_s):
        placed=False
        for g in groups:
            head=g[-1]
            d=point_distance_km(head.center_lat,head.center_lon,cell.center_lat,cell.center_lon)
            if d<=overlap_ratio*(head.radius_km+cell.radius_km) and cell.start_s<=head.end_s:
                g.append(cell); placed=True; break
        if not placed: groups.append([cell])
    return groups
