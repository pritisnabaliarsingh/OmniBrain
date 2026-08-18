import os
from pathlib import Path

from dotenv import load_dotenv


# Backend root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from backend folder
load_dotenv(BASE_DIR / ".env")


# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


# JWT configuration
SECRET_KEY = GEMINI_API_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Upload directory
UPLOAD_DIR = BASE_DIR / "uploads"

# Allowed upload file types
ALLOWED_TYPES = {
    "application/pdf"
}

# Maximum upload file size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Create upload directory if it does not exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
