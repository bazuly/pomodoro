from redis import Redis
from schema.task import TaskSchema
import json


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self):
        with self.redis as redis:
            task_json = redis.lrange("tasks", 0, -1)
            if task_json:
                return [TaskSchema.model_validate(json.loads(task)) for task in task_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        task_json = [task.json() for task in tasks]
        if task_json:
            with self.redis as redis:
                redis.lpush("tasks", *task_json)
        else:
            raise ValueError("Task list is empty")
