from fastapi import FastAPI

from app.tasks.handlers import router as task_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_profile_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_profile_router)
app.include_router(task_router)
