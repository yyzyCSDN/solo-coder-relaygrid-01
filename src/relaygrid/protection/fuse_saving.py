from __future__ import annotations

def should_fast_trip(recloser_fast_s: float, fuse_melt_s: float, margin_s: float=0.05): return recloser_fast_s+margin_s < fuse_melt_s

def shots_to_lockout(sequence: list[str]):
    count=0
    for mode in sequence:
        count+=1
        if mode=="lockout": return count
    return len(sequence)
