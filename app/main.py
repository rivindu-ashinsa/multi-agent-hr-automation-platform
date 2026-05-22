from fastapi import FastAPI

from app.api.routes import router

from app.core.database import init_db


app = FastAPI()

init_db()

app.include_router(router)