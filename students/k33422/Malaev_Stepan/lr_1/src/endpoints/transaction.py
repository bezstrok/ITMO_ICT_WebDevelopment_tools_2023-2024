import typing as tp

from fastapi import APIRouter, Depends, Query
from sqlalchemy import sql

from .. import schemas, dependencies, models, enums
from ..services.pagination import Paginator
from ..services.repository import Repository


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=schemas.Page[schemas.TransactionGetDTO])
async def get_transactions(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    page: tp.Annotated[int, Query()] = 1,
    transaction_type: tp.Annotated[tp.Optional[enums.TransactionType], Query()] = None,
    orders: tp.Annotated[
        tp.Optional[
            tp.Sequence[
                tp.Literal[
                    "amount",
                    "-amount",
                ]
            ]
        ],
        Query(),
    ] = None,
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> schemas.Page[schemas.TransactionGetDTO]:
    filters: dict[str, tp.Any] = dict(user=user)
    if transaction_type is not None:
        filters.update(transaction_type=transaction_type)
    limit, offset = Paginator.page_to_limit_offset(models.Transaction, page=page)

    transactions = await models.Transaction.get_many(
        filters,
        limit=limit,
        offset=offset,
        orders=orders,
        session=session,
    )

    return Paginator.paginate(
        models.Transaction,
        list(map(schemas.TransactionGetDTO.model_validate, transactions)),
        page=page,
    )


@router.post("", response_model=schemas.TransactionGetDTO)
async def create_transaction(
    schema: schemas.TransactionCUDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> schemas.TransactionGetDTO:
    data = dict(**schema.model_dump(), user=user)

    transaction = await models.Transaction.create_one(data, result=True, session=session)
    await session.commit()

    return schemas.TransactionGetDTO.model_validate(transaction)


@router.get("/{transaction_id}", response_model=schemas.TransactionGetDTO)
async def get_transaction(
    transaction: tp.Annotated[models.Transaction, Depends(dependencies.get_transaction)],
) -> schemas.TransactionGetDTO:
    return schemas.TransactionGetDTO.model_validate(transaction)


@router.put("/{transaction_id}", response_model=schemas.TransactionGetDTO)
async def update_transaction(
    schema: schemas.TransactionCUDTO,
    transaction: tp.Annotated[models.Transaction, Depends(dependencies.get_transaction)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> schemas.TransactionGetDTO:
    await transaction.update_self(schema.model_dump(), result=True, session=session)
    await session.commit()

    return schemas.TransactionGetDTO.model_validate(transaction)


@router.delete("/{transaction_id}", response_model=str)
async def delete_transaction(
    transaction: tp.Annotated[models.Transaction, Depends(dependencies.get_transaction)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> str:
    await transaction.delete_self(session=session)
    await session.commit()

    return "OK"


@router.get("/{transaction_id}/categories", response_model=schemas.Page[schemas.CategoryGetManyDTO])
async def get_transaction_categories(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    transaction: tp.Annotated[models.Transaction, Depends(dependencies.get_transaction)],
    page: tp.Annotated[int, Query()] = 1,
    parent_id: tp.Annotated[tp.Optional[int], Query()] = None,
    budget_id: tp.Annotated[tp.Optional[int], Query()] = None,
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> schemas.Page[schemas.CategoryGetManyDTO]:
    filters: dict[str, tp.Any] = dict(user=user)
    if parent_id is not None:
        filters.update(parent_id=parent_id)
    if budget_id is not None:
        filters.update(budget_id=budget_id)
    limit, offset = Paginator.page_to_limit_offset(models.Category, page=page)

    statement = (
        sql.select(models.Category)
        .join(
            models.TransactionCategory,
            (
                (models.TransactionCategory.category_id == models.Category.id)
                & (models.TransactionCategory.user_id == models.Category.user_id)
            ),
        )
        .where(
            models.TransactionCategory.transaction_id == transaction.id,  # noqa
            *Repository.build_django_filters(models.Category, filters),
        )
        .limit(limit)
        .offset(offset)
    )

    execution = await session.execute(statement)
    categories = execution.scalars().all()

    return Paginator.paginate(
        models.Category,
        list(map(schemas.CategoryGetManyDTO.model_validate, categories)),
        page=page,
    )
