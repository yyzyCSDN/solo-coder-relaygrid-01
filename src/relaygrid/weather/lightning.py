from __future__ import annotations

def correlate_strikes(strikes: list[tuple[float,float,float]], asset_points: list[tuple[str,float,float]], radius_deg: float=0.02):
    out=[]
    for ts,lat,lon in strikes:
        for aid,alat,alon in asset_points:
            if (lat-alat)**2+(lon-alon)**2 <= radius_deg**2: out.append((ts,aid))
    return out

def storm_window(events: list[float], gap_s: float=900.0):
    if not events: return []
    events=sorted(events); windows=[]; start=prev=events[0]
    for t in events[1:]:
        if t-prev>gap_s: windows.append((start,prev)); start=t
        prev=t
    windows.append((start,prev)); return windows
