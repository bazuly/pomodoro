from redis import asyncio as Redis
from schema.task import TaskSchema
import json


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self):
        task_json_list = await self.redis.lrange("tasks", 0, -1)
        if task_json_list:
            return [TaskSchema.model_validate(json.loads(task)) for task in task_json_list]

    async def set_tasks(self, tasks: list[TaskSchema]):
        task_json_list = [task.json() for task in tasks]
        if task_json_list:
            # remove old data from list
            await self.redis.delete("tasks")
            # set new data
            await self.redis.rpush("tasks", task_json_list)
        else:
            raise ValueError("Task list is empty")
