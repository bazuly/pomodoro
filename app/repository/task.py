from typing import List

from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import Session

from app.models import Tasks, Categories
from app.schema.task import TaskCreateSchema


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_task(self, task_id) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        async with self.db_session as session:
            task = (await session.execute(query)).scalar_one_or_none()
        return task

    async def get_tasks(self) -> list[Tasks]:
        async with self.db_session as session:
            tasks: list[Tasks] = (await session.execute(select(Tasks))).scalars().all()
        return tasks

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = (
            insert(Tasks)
            .values(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id)
            .returning(Tasks.id)
        )
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return task_id

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(
            Tasks.id == task_id,
            Tasks.user_id == user_id
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(
            Categories, Tasks.category_id == Categories.id
        ).where(Categories.name == category_name)
        async with self.db_session as session:
            tasks: List[Tasks] = session.execute(query).scalars.all()
            return tasks

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(
            Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            updated_task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            await session.flush()
            if updated_task_id is None:
                raise ValueError(f"Task with id {task_id} not found.")
            return await self.get_task(updated_task_id)

    async def get_user_task(self, user_id: int, task_id: int) -> Tasks:
        query = select(Tasks).where(
            Tasks.id == task_id, Tasks.user_id == user_id)
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task
