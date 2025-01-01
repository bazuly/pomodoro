from fastapi import APIRouter, status, Depends


from schema.task import TaskSchema
from repository import TaskRepository
from dependency import get_tasks_repository

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=list[TaskSchema]
)
async def get_tasks(task_repository: TaskRepository = Depends(get_tasks_repository)):
    tasks = task_repository.get_tasks()
    return tasks


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
