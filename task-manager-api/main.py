from fastapi import FastAPI
from routers import tasks,meta



app=FastAPI()

app.include_router(tasks.router)
app.include_router(meta.router)





