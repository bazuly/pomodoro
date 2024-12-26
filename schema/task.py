from pydantic import BaseModel, model_validator


class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int
    category_id: int

    @model_validator(mode='after')
    def check_name_validator(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Name or pomodoro_count fields is requierd")
        return self