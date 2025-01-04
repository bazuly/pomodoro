from handlers.auth import router as auth_router
from handlers.ping import router as ping_router
from handlers.tasks import router as task_router
from handlers.user import router as user_router


routers = [ping_router, task_router, user_router, auth_router]
