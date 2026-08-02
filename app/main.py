from fastapi import FastAPI

from app.routers import upload
from app.routers import ask
import app.routers.health as health_router

from app.utils.logger import logger

app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 OmniBrain Backend API started successfully.")

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(health_router.router)
    
 