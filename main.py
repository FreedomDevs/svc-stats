from fastapi import FastAPI
from routes import routers
from database import engine
from models import PlayerStats
import uvicorn

app = FastAPI()


@app.on_event("startup")
def startup():
    PlayerStats.metadata.create_all(bind=engine)


for route in routers:
    app.include_router(route)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9005, reload=True)

