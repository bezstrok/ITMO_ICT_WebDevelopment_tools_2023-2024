import typing as tp

from fastapi import Depends, exceptions, status

from . import database, authorization
from .. import schemas, models

__all__ = [
    "get_category",
]


async def get_category(
    category_id: int,
    payload: tp.Annotated[schemas.Payload, Depends(authorization.get_access_payload)],
    session: database.AsyncSession = Depends(database.get_session),
) -> models.Category:
    category = await models.Category.get_one(dict(id=category_id, user_id=payload.sub), session=session)

    if category is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Category not found",
        )

    return category
