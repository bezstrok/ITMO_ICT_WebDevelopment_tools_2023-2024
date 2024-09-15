import typing as tp

from fastapi import APIRouter, Depends, HTTPException, status

from .. import schemas, dependencies, models


router = APIRouter(prefix="/relationships", tags=["Relationships"])


@router.post("/categoryToTransaction", response_model=str)
async def create_relationship_category_to_transaction(
    schema: schemas.CategoryToTransactionDTO,
    payload: tp.Annotated[schemas.Payload, Depends(dependencies.get_access_payload)],
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> str:
    transaction = await dependencies.get_transaction(schema.transaction_id, payload, session)
    category = await dependencies.get_category(schema.category_id, payload, session)
    filters: dict[str, tp.Any] = dict(transaction_id=transaction.id, category_id=category.id, user_id=user.id)

    relationship = await models.TransactionCategory.get_one(filters, session=session)
    if relationship is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Relationship already exists")

    await models.TransactionCategory.create_one(filters, session=session)
    await session.commit()

    return "OK"
