from dependency import (
    get_tasks_repository,
    get_tasks_cache_repository,
    get_task_service
)

from repository import TaskRepository, TaskCache

from fastapi import APIRouter, status, Depends

from typing import Annotated

from schema.task import TaskSchema
from service.task import TaskService


router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=list[TaskSchema]
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()


@router.post(
    "/",
    response_model=TaskSchema
)
async def create_task(
    task: TaskSchema,
    task_repository: TaskRepository = Depends(get_tasks_repository)
):
    task_repository.create_task(task)
    return task


@router.patch(
    "/{task_id}",
)
async def patch_task(
    task_id: int,
    new_task_name: str,
    task_repository: TaskRepository = Depends(get_tasks_repository)
):
    updated_task = task_repository.update_task_name(task_id, new_task_name)
    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    task_repository: TaskRepository = Depends(get_tasks_repository)
):
    task_repository.delete_task(task_id)
    return {"task deleted": f"task_id: {task_id}"}


@router.get(
    "/{category_name}",
)
async def get_task_by_category_name(
    category_name: int,
    task_repository: TaskRepository = Depends(get_tasks_repository)
):
    category_task_object = task_repository.get_task_by_category_name(
        category_name)
    return category_task_object
