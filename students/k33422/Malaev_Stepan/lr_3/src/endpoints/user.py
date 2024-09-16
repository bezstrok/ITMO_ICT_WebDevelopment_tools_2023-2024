import typing as tp

from fastapi import APIRouter, Depends

from .. import schemas, dependencies, models


router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=schemas.UserGetDTO)
async def get_user(
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
) -> schemas.UserGetDTO:
    return schemas.UserGetDTO.model_validate(user)


@router.put("", response_model=schemas.UserGetDTO)
async def update_user(
    schema: schemas.UserUpdateDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.UserGetDTO:
    await user.update_self(schema.model_dump(), result=True, session=session)
    await session.commit()

    return schemas.UserGetDTO.model_validate(user)
