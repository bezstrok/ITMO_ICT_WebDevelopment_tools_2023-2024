import typing as tp

import jwt
from fastapi import Depends, security, exceptions, status

from .. import schemas
from ..services.authorization import decode_jwt

__all__ = [
    "get_payload",
    "get_access_payload",
    "get_refresh_payload",
]


def get_http_bearer_token(
    credentials: tp.Annotated[security.HTTPAuthorizationCredentials, Depends(security.HTTPBearer())],
) -> str:
    return credentials.credentials


def get_payload(token: tp.Annotated[str, Depends(get_http_bearer_token)]) -> schemas.Payload:
    try:
        payload = decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise exceptions.HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except jwt.InvalidTokenError:
        raise exceptions.HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    return schemas.Payload.model_validate(payload)


def get_access_payload(payload: tp.Annotated[schemas.Payload, Depends(get_payload)]) -> schemas.Payload:
    if payload.typ != "access":
        raise exceptions.HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type (access required)")

    return payload


def get_refresh_payload(payload: tp.Annotated[schemas.Payload, Depends(get_payload)]) -> schemas.Payload:
    if payload.typ != "refresh":
        raise exceptions.HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token type (refresh required)")

    return payload
