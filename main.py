from fastapi import FastAPI
from api.calendar_routes import router as calendar_router

app = FastAPI()

app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
