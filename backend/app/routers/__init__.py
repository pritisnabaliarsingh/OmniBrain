from fastapi import APIRouter
from app.routers import ask
from app.routers import upload
from app.routers import health
from app.routers import vision
api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(ask.router)
api_router.include_router(vision.router)
