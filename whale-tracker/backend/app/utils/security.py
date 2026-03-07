import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = int((datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)).timestamp())
    body = json.dumps(payload, separators=(",", ":")).encode()
    sig = hmac.new(settings.secret_key.encode(), body, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(body + b"." + sig).decode()
