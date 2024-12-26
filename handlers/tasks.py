from fastapi import APIRouter
from schema.task import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=list[Task]
)
async def get_task():
    return {"data": {"test_data": "test_data"}}


@router.post("/", response_model=Task)
async def create_task(task: Task):
    return task
