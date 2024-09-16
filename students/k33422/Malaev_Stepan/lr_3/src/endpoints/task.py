import typing as tp

from fastapi import APIRouter, Depends, HTTPException, status
from taskiq_redis.exceptions import ResultIsMissingError

from .. import schemas, dependencies, models, tasks
from ..worker import result_backend


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/parseUsers", response_model=schemas.Task[schemas.ParseUsersGetDTO])
async def create_parse_users_task(
    schema: schemas.ParseUsersCreateDTO,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
) -> schemas.Task[schemas.ParseUsersGetDTO]:
    task = await tasks.parse_users.kiq(schema.pages)  # type: ignore[call-overload]

    result: tp.Optional[schemas.ParseUsersGetDTO] = None
    if await task.is_ready():
        result = await task.get_result()

    return schemas.Task(id=task.task_id, result=result)


@router.get("/parseUsers/{task_id}", response_model=schemas.Task[schemas.ParseUsersGetDTO])
async def get_parse_users_task(
    task_id: str,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
) -> schemas.Task[schemas.ParseUsersGetDTO]:
    try:
        result = await result_backend.get_result(task_id)
    except ResultIsMissingError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")

    return schemas.Task(id=task_id, result=result.return_value)
