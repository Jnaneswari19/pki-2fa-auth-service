import os

DATA_DIR = os.getenv("DATA_DIR", "/app/data")
SEED_PATH = os.path.join(DATA_DIR, "seed.txt")
CRON_LOG = os.path.join(DATA_DIR, "cron.log")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Instructor-aligned key filenames (committed at repo root, copied into /app)
STUDENT_PRIV_PATH = os.getenv("STUDENT_PRIV_PATH", "/app/student_private.pem")
STUDENT_PUB_PATH = os.getenv("STUDENT_PUB_PATH", "/app/student_public.pem")
INSTRUCTOR_PUB_PATH = os.getenv("INSTRUCTOR_PUB_PATH", "/app/instructor_public.pem")
