from fastapi import FastAPI

from app.routers import api_router
from app.utils.logger import logger
from app.database.models import Base
from app.database.db import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 OmniBrain Backend API started successfully.")


@app.get("/")
def root():
    return {"message": "Welcome to OmniBrain Backend API"}


app.include_router(api_router)
