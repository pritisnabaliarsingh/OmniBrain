from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter(tags=["Health"])
@router.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to OmniBrain Backend API"
    }
    # Health endpoint
@router.get("/health")
def health():
    logger.info("Health endpoint accessed")
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }
