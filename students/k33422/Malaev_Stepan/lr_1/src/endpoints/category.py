import typing as tp

from fastapi import APIRouter, Depends, Query
from sqlalchemy import orm

from .. import schemas, dependencies, models
from ..services.pagination import Paginator


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=schemas.Page[schemas.CategoryGetManyDTO])
async def get_categories(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
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
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
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
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
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
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
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
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
) -> str:
    await category.delete_self(session=session)
    await session.commit()

    return "OK"


# @router.get("/{category_id}/transactions", response_model=schemas.Page[schemas.TransactionGetManyDTO])
