from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import Tasks, get_db_connection, Categories


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            task = session.execute(query)
        return task

    def get_tasks(self) -> Tasks | None:
        with self.db_session as session:
            tasks: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return tasks

    def create_task(self, task: Tasks) -> None:
        with self.db_session as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(
            Categories, Tasks.category_id == Categories.id
        ).where(Categories.name == category_name)
        with self.db_session as session:
            tasks: List[tasks] = session.execute(query).scalars.all()
            session.commit()


def get_tasks_repository() -> TaskRepository:
    db_session = get_db_connection()
    return TaskRepository(db_session)
