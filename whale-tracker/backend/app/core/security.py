import base64
from datetime import datetime, timedelta, timezone
from app.core.config import settings


def hash_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def create_access_token(subject: str) -> str:
    exp = int((datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)).timestamp())
    raw = f'{subject}:{exp}:{settings.secret_key}'
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_access_token(token: str) -> str | None:
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        subject, exp, secret = raw.split(':', 2)
        if secret != settings.secret_key or int(exp) < int(datetime.now(timezone.utc).timestamp()):
            return None
        return subject
    except Exception:
        return None
