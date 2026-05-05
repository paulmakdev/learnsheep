from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
import time
import uuid
import base64
from app.schemas.auth import TokenClaim


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(session_dict) -> str:
    return jwt.encode(session_dict, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def create_uuid4_compact():
    u = uuid.uuid4()
    return base64.urlsafe_b64encode(u.bytes).rstrip(b"=").decode("ascii")


def get_current_time_seconds():
    return int(time.time())


def create_access_token_dict(
    user_id, max_idle_seconds=60 * 60 * 24 * 7, max_life_seconds=60 * 60 * 24 * 30
) -> TokenClaim:
    now = get_current_time_seconds()
    access_token_dict = {
        # session id
        "sid": create_uuid4_compact(),
        # user id
        "uid": str(user_id),
        # issued at
        "iat": now,
        # last refreshed at
        "lra": now,
        # idle expire at
        "iea": now + min(settings.access_token_expire_minutes * 60, max_life_seconds),
        # max expire at
        "mea": now + max_life_seconds,
    }
    return access_token_dict


def update_access_token_dict(access_token_dict, max_idle_seconds=60 * 60 * 24 * 7):
    now = get_current_time_seconds()
    access_token_dict.lra = now
    access_token_dict.iea = min(now + max_idle_seconds, access_token_dict.mea)
    return access_token_dict
