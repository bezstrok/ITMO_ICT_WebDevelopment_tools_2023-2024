import typing as tp

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie

from .. import schemas, dependencies, models, config
from ..services.authorization import hash_password, check_password, create_jwt


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/register", response_model=schemas.UserGetDTO)
async def register(
    schema: schemas.CredentialsDTO,
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.UserGetDTO:
    is_exists = await models.User.exists(dict(username=schema.username), session=session)
    if is_exists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")

    user = await models.User.create_one(
        dict(
            username=schema.username,
            hashed_password=hash_password(schema.password),
        ),
        result=True,
        session=session,
    )
    await session.commit()

    return schemas.UserGetDTO.model_validate(user)


@router.post("/login", response_model=schemas.AccessTokenDTO)
async def login(
    schema: schemas.CredentialsDTO,
    response: Response,
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> schemas.AccessTokenDTO:
    user = await models.User.get_one(dict(username=schema.username), session=session)
    if user is None or not check_password(schema.password, user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect username or password")

    response.set_cookie(
        key="refresh_token",
        value=create_jwt(user.id, "refresh"),
        httponly=True,
        samesite="lax",
        expires=config.authorization.refresh_token_expires_in,
    )

    return schemas.AccessTokenDTO(access_token=create_jwt(user.id, "access"))


@router.post("/refreshToken", response_model=schemas.AccessTokenDTO)
def refresh_access_token(
    refresh_token: tp.Annotated[tp.Optional[str], Cookie()] = None,
) -> schemas.AccessTokenDTO:
    if refresh_token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is missing")

    payload = dependencies.get_refresh_payload(dependencies.get_payload(refresh_token))

    return schemas.AccessTokenDTO(access_token=create_jwt(payload.sub, "access"))


@router.post("/changePassword", response_model=str)
async def change_password(
    schema: schemas.ChangePasswordDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_database_session),
) -> str:
    if not check_password(schema.old_password, user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect password")

    await user.update_self(dict(hashed_password=user.hashed_password), session=session)
    await session.commit()

    return "OK"
