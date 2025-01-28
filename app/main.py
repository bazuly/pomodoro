from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.broker.consumer import make_amqp_consumer
from app.tasks.handlers import router as task_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_consumer()
    yield


app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_profile_router)
app.include_router(task_router)
