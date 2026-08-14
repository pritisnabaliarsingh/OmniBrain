import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")