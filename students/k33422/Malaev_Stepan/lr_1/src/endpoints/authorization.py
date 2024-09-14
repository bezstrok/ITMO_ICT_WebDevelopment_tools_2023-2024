# from fastapi import APIRouter, Depends
#
# from .. import schemas, dependencies
#
#
# router = APIRouter(prefix="/auth", tags=["Authorization"])
#
#
# @router.post("/register", response_model=...)
# async def register(
#     schema: schemas.CredentialsDTO,
#     session: dependencies.AsyncSession = Depends(dependencies.get_session),
# ): ...
#
#
# @router.post("/login", response_model=schemas.AccessTokenDTO)
# async def login(
#     schema: schemas.CredentialsDTO,
#     session: dependencies.AsyncSession = Depends(dependencies.get_session),
# ): ...
#
#
# @router.post("/refreshToken", response_model=schemas.AccessTokenDTO)
# def refresh(): ...
#
#
# @router.post("/changePassword", response_model=...)
# async def change_password(
#     schema: ...,
#     session: dependencies.AsyncSession = Depends(dependencies.get_session),
# ): ...
