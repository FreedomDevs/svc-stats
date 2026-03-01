from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import routers
from database import engine
from models import PlayerStats
import uvicorn
from settings import settings

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

