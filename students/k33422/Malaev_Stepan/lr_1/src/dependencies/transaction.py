import typing as tp

from fastapi import Depends, exceptions, status

from . import database, authorization
from .. import schemas, models

__all__ = [
    "get_transaction",
]


async def get_transaction(
    transaction_id: int,
    payload: tp.Annotated[schemas.Payload, Depends(authorization.get_access_payload)],
    session: database.AsyncSession = Depends(database.get_session),
) -> models.Transaction:
    transaction = await models.Transaction.get_one(dict(id=transaction_id, user_id=payload.sub), session=session)

    if transaction is None:
        raise exceptions.HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Transaction not found",
        )

    return transaction
