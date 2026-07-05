"""
Cấu hình chung cho toàn bộ dự án BankBot.
Load biến môi trường từ file .env và khai báo các hằng số.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# === Đường dẫn gốc của dự án ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === LLM Configuration ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL_NAME = "gemini-1.5-flash"

# === Embedding Configuration ===
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# === Data Paths ===
RAW_DATA_DIR = str(BASE_DIR / "data" / "raw")
PROCESSED_DATA_DIR = str(BASE_DIR / "data" / "processed")
VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", str(BASE_DIR / "data" / "vector_db"))

# === Chunking Configuration ===
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# === API Configuration ===
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
