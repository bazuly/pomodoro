import json
from typing import List, Optional

from redis import asyncio as Redis
from app.tasks.schema import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_tasks(self, tasks: list[TaskSchema]):
        task_json_list = [json.dumps(task.dict()) for task in tasks]
        if task_json_list:
            # remove old data from list
            await self.redis.delete("tasks")
            # set new data
            await self.redis.rpush("tasks", *task_json_list)
        else:
            raise ValueError("Task list is empty")

    async def get_tasks(self) -> Optional[List[TaskSchema]]:
        task_json_list = await self.redis.lrange("tasks", 0, -1)
        if task_json_list:
            try:
                return [TaskSchema.model_validate(json.loads(task)) for task in task_json_list]
            except json.JSONDecodeError as e:
                raise ValueError("Invalid task data in Redis") from e
        return None
