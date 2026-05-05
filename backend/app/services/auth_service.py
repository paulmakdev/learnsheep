from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    TokenClaim,
    RevocationRequest,
    PublicSessionResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    update_access_token_dict,
    create_access_token_dict,
    create_uuid4_compact,
)
from app.core.cache import CacheService
import json
from app.schemas.info import DeviceInfo


def register_user(
    db: Session, cache: CacheService, data: RegisterRequest, device_info: DeviceInfo
) -> TokenResponse:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("Email already registered")

    user = User(
        email=data.email,
        # bcrypt automatically salts the password, pretty neat, it is part of the output
        hashed_salted_password=hash_password(data.password),
        display_name=data.display_name or data.email.split("@")[0],
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    session_dict = create_access_token_dict(user_id=str(user.id))
    access_token = create_access_token(session_dict)

    session_holder_ttl = max(session_dict["mea"] - session_dict["lra"], 1)
    session_ttl = max(int((session_dict["iea"] - session_dict["lra"]) * 1.5), 1)

    cache.sadd(
        "user:" + str(user.id) + ":sessions",
        session_dict["sid"],
        ttl=session_holder_ttl,
    )

    session_info = {
        "device_info": device_info,
        "iat": session_dict["iat"],
        "revoked": False,
    }

    cache.set("session:" + session_dict["sid"], session_info, ttl=session_ttl)

    return {"access_token": access_token, "access_token_type": "bearer"}


def login_user(
    db: Session, cache: CacheService, data: LoginRequest, device_info: DeviceInfo
) -> TokenResponse:
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_salted_password):
        raise ValueError(
            "Invalid credentials"
        )  # Same error for both cases — intentional

    session_dict = create_access_token_dict(user_id=str(user.id))
    access_token = create_access_token(session_dict)

    # remove all old sessions because we want to make sure we don't get a bloated list from many logins
    current_session_ids = cache.smembers("user:" + str(user.id) + ":sessions")

    if current_session_ids:
        for session_id in current_session_ids:
            if not cache.get("session:" + session_id):
                cache.srem("user:" + str(user.id) + ":sessions", session_id)

    session_holder_ttl = max(session_dict["mea"] - session_dict["lra"], 1)
    session_ttl = max(int((session_dict["iea"] - session_dict["lra"]) * 1.5), 1)

    cache.sadd(
        "user:" + str(user.id) + ":sessions",
        session_dict["sid"],
        ttl=session_holder_ttl,
    )

    session_info = {
        "device_info": device_info,
        "iat": session_dict["iat"],
        "revoked": False,
    }

    cache.set("session:" + session_dict["sid"], session_info, ttl=session_ttl)

    return {"access_token": access_token, "access_token_type": "bearer"}


def refresh_access(token_claim: TokenClaim) -> TokenResponse:
    # Validity of token claim is handled when getting token_claim.

    new_token_claim = update_access_token_dict(token_claim)
    new_access_token = create_access_token(new_token_claim.model_dump())

    return {"access_token": new_access_token, "access_token_type": "bearer"}


def get_public_session_id(
    cache: CacheService, current_user: User
) -> PublicSessionResponse:

    current_private_session_ids = cache.smembers(
        "user:" + str(current_user.id) + ":sessions"
    )

    public_to_private_ids = {}
    public_info = []
    if current_private_session_ids:
        for private_session_id in current_private_session_ids:
            private_session_info = cache.get("session:" + private_session_id)
            if private_session_info:
                public_session_id = create_uuid4_compact()
                public_to_private_ids[public_session_id] = private_session_id
                public_info.append(
                    {
                        "session_id": public_session_id,
                        "session_info": private_session_info,
                    }
                )
            else:
                cache.srem(
                    "user:" + str(current_user.id) + ":sessions", private_session_id
                )
        cache.set(
            "user:" + str(current_user.id) + ":sessions:public_to_private",
            public_to_private_ids,
        )

    return {"sessions": public_info}


def revoke_session_with_public_id(
    cache: CacheService,
    current_user: User,
    data: RevocationRequest,
) -> TokenResponse:

    revocation_ids = data.ids_to_revoke
    public_to_private_ids = cache.get(
        "user:" + str(current_user.id) + ":sessions:public_to_private"
    )
    revoked_ids = []
    for revocation_id in revocation_ids:
        if revocation_id in public_to_private_ids:
            private_session_id = public_to_private_ids[revocation_id]
            session_info = cache.get("session:" + private_session_id)
            session_info["revoked"] = True
            cache.set_preserve_ttl(
                "session:" + private_session_id, json.dumps(session_info)
            )
            cache.srem("user:" + str(current_user.id) + ":sessions", private_session_id)
            revoked_ids.append(revocation_id)

    return {"revoked_ids": revoked_ids}
