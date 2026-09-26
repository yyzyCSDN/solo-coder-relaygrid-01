from __future__ import annotations
import hmac, hashlib

def sign_command(secret: bytes, device_id: str, nonce: str, action: str) -> str:
    payload=f"{device_id}|{nonce}|{action}".encode(); return hmac.new(secret,payload,hashlib.sha256).hexdigest()

def verify_command(secret: bytes, device_id: str, nonce: str, action: str, signature: str) -> bool:
    return hmac.compare_digest(sign_command(secret,device_id,nonce,action),signature)

def nonce_fresh(nonce_timestamp_s: float, now_s: float, max_age_s: float=30.0):
    age=now_s-nonce_timestamp_s; return 0.0<=age<=max_age_s
