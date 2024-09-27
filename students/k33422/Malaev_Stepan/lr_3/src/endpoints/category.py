import typing as tp

from fastapi import APIRouter, Depends, Query
from sqlalchemy import orm, sql

from .. import schemas, dependencies, models, enums
from ..services.pagination import Paginator
from ..services.repository import Repository


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=schemas.Page[schemas.CategoryGetManyDTO])
async def get_categories(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    page: tp.Annotated[int, Query()] = 1,
    parent_id: tp.Annotated[tp.Optional[int], Query()] = None,
    budget_id: tp.Annotated[tp.Optional[int], Query()] = None,
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.Page[schemas.CategoryGetManyDTO]:
    filters: dict[str, tp.Any] = dict(user=user)
    if parent_id is not None:
        filters.update(parent_id=parent_id)
    if budget_id is not None:
        filters.update(budget_id=budget_id)
    limit, offset = Paginator.page_to_limit_offset(models.Category, page=page)

    categories = await models.Category.get_many(
        filters,
        limit=limit,
        offset=offset,
        session=session,
    )

    return Paginator.paginate(
        models.Category,
        list(map(schemas.CategoryGetManyDTO.model_validate, categories)),
        page=page,
    )


@router.post("", response_model=schemas.CategoryGetOneDTO)
async def create_category(
    schema: schemas.CategoryCUDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.CategoryGetOneDTO:
    data = dict(**schema.model_dump(), user=user)

    created_category: models.Category = await models.Category.create_one(data, result=True, session=session)  # type: ignore
    await session.commit()

    category = await models.Category.get_one(
        dict(id=created_category.id),
        loads=[
            orm.joinedload(models.Category.parent),
            orm.joinedload(models.Category.budget),
            orm.selectinload(models.Category.children),
        ],
        session=session,
    )

    return schemas.CategoryGetOneDTO.model_validate(category)


@router.get("/{category_id}", response_model=schemas.CategoryGetOneDTO)
async def get_category(
    category: tp.Annotated[models.Category, Depends(dependencies.get_category)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.CategoryGetOneDTO:
    category: models.Category = await models.Category.get_one(  # type: ignore
        dict(id=category.id),
        loads=[
            orm.joinedload(models.Category.parent),
            orm.joinedload(models.Category.budget),
            orm.selectinload(models.Category.children),
        ],
        session=session,
    )

    return schemas.CategoryGetOneDTO.model_validate(category)


@router.put("/{category_id}", response_model=schemas.CategoryGetOneDTO)
async def update_category(
    schema: schemas.CategoryCUDTO,
    category: tp.Annotated[models.Category, Depends(dependencies.get_category)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.CategoryGetOneDTO:
    await category.update_self(schema.model_dump(), session=session)
    await session.commit()

    category: models.Category = await models.Category.get_one(  # type: ignore
        dict(id=category.id),
        loads=[
            orm.joinedload(models.Category.parent),
            orm.joinedload(models.Category.budget),
            orm.selectinload(models.Category.children),
        ],
        session=session,
    )

    return schemas.CategoryGetOneDTO.model_validate(category)


@router.delete("/{category_id}", response_model=str)
async def delete_category(
    category: tp.Annotated[models.Category, Depends(dependencies.get_category)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> str:
    await category.delete_self(session=session)
    await session.commit()

    return "OK"


@router.get("/{category_id}/transactions", response_model=schemas.Page[schemas.TransactionGetDTO])
async def get_category_transactions(
    category: tp.Annotated[models.Category, Depends(dependencies.get_category)],
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
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.Page[schemas.TransactionGetDTO]:
    filters: dict[str, tp.Any] = dict(user=user)
    if transaction_type is not None:
        filters.update(transaction_type=transaction_type)
    if orders is None:
        orders = []
    limit, offset = Paginator.page_to_limit_offset(models.Transaction, page=page)

    statement = (
        sql.select(models.Transaction)
        .join(
            models.TransactionCategory,
            (
                (models.TransactionCategory.transaction_id == models.Transaction.id)
                & (models.TransactionCategory.user_id == models.Transaction.user_id)
            ),
        )
        .where(
            models.TransactionCategory.category_id == category.id,  # noqa
            *Repository.build_django_filters(models.Transaction, filters),
        )
        .limit(limit)
        .offset(offset)
        .order_by(*Repository.build_django_orders(models.Transaction, orders))
    )

    execution = await session.execute(statement)
    transactions = execution.scalars().all()

    return Paginator.paginate(
        models.Transaction,
        list(map(schemas.TransactionGetDTO.model_validate, transactions)),
        page=page,
    )
