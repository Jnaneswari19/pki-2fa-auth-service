import os
from app.config import DATA_DIR

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def write_text(path: str, content: str):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def file_exists(path: str) -> bool:
    return os.path.exists(path)
