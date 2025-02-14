from pydantic import BaseModel, model_validator


class TaskSchema(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int
    category_id: int
    user_id: int | str

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def check_name_validator(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("Name or pomodoro_count fields is required")
        return self


class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int
    category_id: int
