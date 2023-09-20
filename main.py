from fastapi import FastAPI
from mangum import Mangum
from api.routes.calendar_routes import router as calendar_router

app = FastAPI()

app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])

handler = Mangum(app)
