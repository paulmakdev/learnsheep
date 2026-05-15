from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    TokenClaim,
    PublicSessionResponse,
    RevocationRequest,
    OkResponse,
)
from app.services.auth_service import (
    register_user,
    login_user,
    refresh_access,
    get_public_session_id,
    revoke_session_with_public_id,
    make_temp_user,
)
from app.core.database import get_db
from app.core.cache import get_redis, CacheService
from app.core.info import (
    get_device_info,
    get_token_claim,
    get_current_user,
    get_token_claim_non_blocking,
)
from app.schemas.info import DeviceInfo
from app.core.security import set_auth_cookie
from typing import Optional
import logging


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(
    data: RegisterRequest,
    cache: CacheService = Depends(get_redis),
    token_claim: Optional[TokenClaim] = Depends(get_token_claim_non_blocking),
    db: Session = Depends(get_db),
    device_info: DeviceInfo = Depends(get_device_info),
):
    try:
        return register_user(db, cache, data, device_info, token_claim)
    except ValueError as e:
        logging.exception("Error registering.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/register-web", response_model=OkResponse, status_code=201)
def register_web(
    response: Response,
    data: RegisterRequest,
    cache: CacheService = Depends(get_redis),
    token_claim: Optional[TokenClaim] = Depends(get_token_claim_non_blocking),
    db: Session = Depends(get_db),
    device_info: DeviceInfo = Depends(get_device_info),
):
    try:
        access_dict = register_user(db, cache, data, device_info, token_claim)
        set_auth_cookie(response=response, access_token=access_dict["access_token"])
        return {"ok": True}
    except ValueError as e:
        logging.exception("Error registering.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    cache: CacheService = Depends(get_redis),
    db: Session = Depends(get_db),
    device_info: DeviceInfo = Depends(get_device_info),
):
    try:
        return login_user(db, cache, data, device_info)
    except ValueError as e:
        logging.exception("Error loggin in.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/login-web", response_model=OkResponse)
def login_web(
    response: Response,
    data: LoginRequest,
    cache: CacheService = Depends(get_redis),
    db: Session = Depends(get_db),
    device_info: DeviceInfo = Depends(get_device_info),
):
    try:
        access_dict = login_user(db, cache, data, device_info)
        set_auth_cookie(response=response, access_token=access_dict["access_token"])
        return {"ok": True}

    except ValueError as e:
        logging.exception("Error loggin in.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh(token_claim: TokenClaim = Depends(get_token_claim)):
    try:
        return refresh_access(token_claim)
    except ValueError as e:
        logging.exception("Error on refresh.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh-web", response_model=OkResponse)
def refresh_web(response: Response, token_claim: TokenClaim = Depends(get_token_claim)):
    try:
        access_dict = refresh_access(token_claim)
        set_auth_cookie(response=response, access_token=access_dict["access_token"])
        return {"ok": True}
    except ValueError as e:
        logging.exception("Error on refresh.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/sessions-info", response_model=PublicSessionResponse)
def get_sessions_info(
    cache: CacheService = Depends(get_redis),
    current_user=Depends(get_current_user),
):
    try:
        return get_public_session_id(cache, current_user)
    except ValueError as e:
        logging.exception("Error.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/revoke-sessions")
def revoke_sessions(
    data: RevocationRequest,
    cache: CacheService = Depends(get_redis),
    current_user=Depends(get_current_user),
):
    try:
        return revoke_session_with_public_id(
            cache=cache, current_user=current_user, data=data
        )
    except ValueError as e:
        logging.exception("Error.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/temp-credentials-web", response_model=OkResponse, status_code=201)
def temp_credentials_web(
    response: Response,
    cache: CacheService = Depends(get_redis),
    db: Session = Depends(get_db),
    device_info: DeviceInfo = Depends(get_device_info),
):
    try:
        access_dict = make_temp_user(db, cache, device_info)
        set_auth_cookie(response=response, access_token=access_dict["access_token"])
        return {"ok": True}
    except ValueError as e:
        logging.exception("Error.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
