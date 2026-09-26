from __future__ import annotations
import math
EARTH_KM=6371.0088

def haversine_km(lat1,lon1,lat2,lon2):
    p1,p2=math.radians(lat1),math.radians(lat2); dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1)
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*EARTH_KM*math.asin(min(1.0,math.sqrt(a)))

def polyline_length_km(points):
    return sum(haversine_km(*a,*b) for a,b in zip(points,points[1:]))

def nearest_asset(lat,lon,assets):
    ranked=[(haversine_km(lat,lon,alat,alon),aid) for aid,alat,alon in assets]
    return min(ranked) if ranked else None
