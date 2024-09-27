import typing as tp
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from .. import config, schemas

__all__ = [
    "encode_jwt",
    "decode_jwt",
    "create_jwt",
    "hash_password",
    "check_password",
]

Payload = dict[str, tp.Any]


def encode_jwt(
    payload: Payload,
    *,
    key: str = config.authorization.private_key,
    algorithm: str = config.authorization.algorithm,
) -> str:
    return jwt.encode(payload, key, algorithm)


def decode_jwt(
    token: str,
    *,
    key: str = config.authorization.public_key,
    algorithm: str = config.authorization.algorithm,
) -> Payload:
    return tp.cast(Payload, jwt.decode(token, key, algorithms=[algorithm]))


def create_jwt(
    user_id: int,
    token_type: tp.Literal["access", "refresh"],
    *,
    access_token_expires_in: int = config.authorization.access_token_expires_in,
    refresh_token_expires_in: int = config.authorization.refresh_token_expires_in,
) -> str:
    sub = user_id
    iat = datetime.now(timezone.utc)
    typ = token_type
    match typ:
        case "access":
            exp = iat + timedelta(seconds=access_token_expires_in)
        case "refresh":
            exp = iat + timedelta(seconds=refresh_token_expires_in)
        case _:
            raise ValueError("Invalid token type")

    return encode_jwt(schemas.Payload(sub=sub, typ=typ, exp=exp, iat=iat).model_dump())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
