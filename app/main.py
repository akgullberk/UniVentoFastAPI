from fastapi import FastAPI, Depends
from app.routes.clubs import router as clubs_router

app = FastAPI()
app.include_router(clubs_router)

