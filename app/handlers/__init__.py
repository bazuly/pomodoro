from app.handlers.auth import router as auth_router
from app.handlers.ping import router as ping_router
from app.handlers.tasks import router as task_router
from app.handlers.user import router as user_router


routers = [ping_router, task_router, user_router, auth_router]
