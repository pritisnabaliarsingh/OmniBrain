import os 
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok = True)
# Validation constants

ALLOWED_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB                                                                                                                                                                                         