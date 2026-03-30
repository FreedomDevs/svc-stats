from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.routes import routers
from app.database import engine
from app.models import PlayerStats
from app.settings import settings

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    PlayerStats.metadata.create_all(bind=engine)
    yield
    # SHUTDOWN (если понадобится)


for route in routers:
    app.include_router(route)

if __name__ == "__main__":
    uvicorn.run("main:app",host=settings.APP_HOST,port=settings.APP_PORT,reload=True)

