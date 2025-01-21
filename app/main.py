from fastapi import FastAPI

from app.handlers.user import router as user_router
from app.handlers.ping import router as ping_router
from app.handlers.auth import router as auth_router
from app.handlers.tasks import router as task_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ping_router)
app.include_router(task_router)
