import typing as tp

from fastapi import Depends, exceptions, status

from . import database, authorization
from .. import schemas, models

__all__ = [
    "get_budget",
]


async def get_budget(
    budget_id: int,
    payload: tp.Annotated[schemas.Payload, Depends(authorization.get_access_payload)],
    session: database.AsyncSession = Depends(database.get_database_session),
) -> models.Budget:
    budget = await models.Budget.get_one(dict(id=budget_id, user_id=payload.sub), session=session)

    if budget is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Budget not found",
        )

    return budget
