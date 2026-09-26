from __future__ import annotations

def verify(required: list[str],completed: set[str]): return [item for item in required if item not in completed]

def completion_ratio(required: list[str],completed: set[str]): return 1.0 if not required else (len(set(required)&completed)/len(set(required)))
