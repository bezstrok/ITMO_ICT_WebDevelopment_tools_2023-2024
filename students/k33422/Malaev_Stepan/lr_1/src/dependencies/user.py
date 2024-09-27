import typing as tp

from fastapi import Depends, exceptions, status

from . import database, authorization
from .. import schemas, models

__all__ = [
    "get_user",
]


async def get_user(
    payload: tp.Annotated[schemas.Payload, Depends(authorization.get_access_payload)],
    session: database.AsyncSession = Depends(database.get_session),
) -> models.User:
    user = await models.User.get_one(dict(id=payload.sub), session=session)

    if user is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND,
            "User not found",
        )

    return user
