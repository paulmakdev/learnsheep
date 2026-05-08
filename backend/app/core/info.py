from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from user_agents import parse
from app.schemas.info import DeviceInfo
from app.core.security import get_current_time_seconds, decode_token
from app.schemas.auth import TokenClaim
from app.core.cache import get_redis, CacheService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_token_claim(
    request: Request,
    cache: CacheService = Depends(get_redis),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        session_token = request.cookies.get("access_token")
        resolved_token = session_token or token
        if not resolved_token:
            raise ValueError("Invalid token")
        # rest of your existing logic using resolved_token
        payload = decode_token(resolved_token)
        token_claim = TokenClaim.model_validate(payload)
        now = get_current_time_seconds()

        if not token_claim or token_claim.iea < now:
            raise ValueError("Invalid token")  # purposefully vague

        session_info = cache.get("session:" + token_claim.sid)

        if not session_info or session_info.get("revoked", True):
            raise ValueError("Invalid token")  # purposefully vague

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token_claim


def get_current_user(
    db: Session = Depends(get_db), token_claim: TokenClaim = Depends(get_token_claim)
) -> User:
    try:
        user_id: str = token_claim.uid
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


def get_device_info(request: Request) -> DeviceInfo:
    ua_string = request.headers.get("user-agent", "")
    ua = parse(ua_string)

    return {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "os_version": ua.os.version_string,
        "device": ua.device.family,
    }
