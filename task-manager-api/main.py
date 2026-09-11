from fastapi import FastAPI

from db import create_db_and_tables
from routers import tasks, meta

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(meta.router)
app.include_router(tasks.router)