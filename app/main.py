from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import logging                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
import os 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
)

logger = logging.getLogger(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)

# Create FastAPI application
app = FastAPI(
    title="OmniBrain Backend API",
    description="Backend API for OmniBrain Multi-Modal RAG Project",
    version="1.0.0"
)
class AskRequest (BaseModel):
    question: str
@app.on_event("startup")
async def startup_event():
   logger.info("🚀 OmniBrain Backend API started successfully.")

# Validation constants
ALLOWED_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
# Root endpoint
@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to OmniBrain Backend API"
    }

# Health endpoint
@app.get("/health")
def health():
    logger.info("Health endpoint accessed")
    return {
        "status": "healthy",
        "message": "Backend is running successfully"
    }

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        logger.warning(
            f"Invalid file type uploaded: {file.filename} ({file.content_type})"
        )
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read the uploaded file
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # Check if the file is empty
    if len(content) == 0:
        logger.warning(f"Empty file uploaded: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        logger.warning(
            f"Large file rejected: {file.filename}, Size: {len(content)} bytes"
        )
        raise HTTPException(
            status_code=400,
            detail="Uploaded file exceeds maximum allowed size of 10 MB."
        )

    # Log successful upload
    logger.info(
        f"File uploaded successfully: {file.filename}, Size: {len(content)} bytes"
    )

    return {
        "filename":file.filename,
        "content_type": file.content_type,
        "size" : len(content),
        "stored_path": file_path,
        "message": "File Uploaded Successfully and stored."
        
    }
    
  # Ask API
@app.post("/ask")
async def ask_question(request: AskRequest):

    # Validate question
    if not request.question.strip():
        logger.warning("Empty question received.")

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    logger.info(f"Question received: {request.question}")

    # Placeholder answer
    answer = "This is a sample response from OmniBrain."

    logger.info("Answer generated successfully.")

    return {
        "question": request.question,
        "answer": answer
    }
    