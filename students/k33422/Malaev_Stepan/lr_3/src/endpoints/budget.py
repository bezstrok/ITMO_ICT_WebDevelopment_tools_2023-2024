import typing as tp
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from .. import schemas, dependencies, models
from ..services.pagination import Paginator


router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("", response_model=schemas.Page[schemas.BudgetGetDTO])
async def get_budgets(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    page: tp.Annotated[int, Query()] = 1,
    start_date: tp.Annotated[tp.Optional[datetime], Query()] = None,
    end_date: tp.Annotated[tp.Optional[datetime], Query()] = None,
    orders: tp.Annotated[
        tp.Optional[
            tp.Sequence[
                tp.Literal[
                    "start_date",
                    "-start_date",
                    "end_date",
                    "-end_date",
                    "amount",
                    "-amount",
                ]
            ]
        ],
        Query(),
    ] = None,
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.Page[schemas.BudgetGetDTO]:
    filters: dict[str, tp.Any] = dict(user=user)
    if start_date is not None:
        filters.update(start_date__ge=start_date)
    if end_date is not None:
        filters.update(end_date__le=end_date)
    limit, offset = Paginator.page_to_limit_offset(models.Budget, page=page)

    budgets = await models.Budget.get_many(
        filters,
        limit=limit,
        offset=offset,
        orders=orders,
        session=session,
    )

    return Paginator.paginate(
        models.Budget,
        list(map(schemas.BudgetGetDTO.model_validate, budgets)),
        page=page,
    )


@router.post("", response_model=schemas.BudgetGetDTO)
async def create_budget(
    schema: schemas.BudgetCUDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.BudgetGetDTO:
    data = dict(**schema.model_dump(), user=user)

    budget = await models.Budget.create_one(data, result=True, session=session)
    await session.commit()

    return schemas.BudgetGetDTO.model_validate(budget)


@router.get("/{budget_id}", response_model=schemas.BudgetGetDTO)
async def get_budget(
    budget: tp.Annotated[models.Budget, Depends(dependencies.get_budget)],
) -> schemas.BudgetGetDTO:
    return schemas.BudgetGetDTO.model_validate(budget)


@router.put("/{budget_id}", response_model=schemas.BudgetGetDTO)
async def update_budget(
    schema: schemas.BudgetCUDTO,
    budget: tp.Annotated[models.Budget, Depends(dependencies.get_budget)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.BudgetGetDTO:
    await budget.update_self(schema.model_dump(), result=True, session=session)
    await session.commit()

    return schemas.BudgetGetDTO.model_validate(budget)


@router.delete("/{budget_id}", response_model=str)
async def delete_budget(
    budget: tp.Annotated[models.Budget, Depends(dependencies.get_budget)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> str:
    await budget.delete_self(session=session)
    await session.commit()

    return "OK"
