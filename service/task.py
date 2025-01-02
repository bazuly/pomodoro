from dataclasses import dataclass
from repository import TaskRepository, TaskCache
from schema.task import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self):
        if cached_tasks := self.task_cache.get_tasks():
            return cached_tasks
        else:
            tasks = self.task_repository.get_tasks()
            task_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(task_schema)
            return task_schema
