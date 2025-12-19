from datetime import datetime
from app.config import CRON_LOG
from app.storage import write_text

def heartbeat():
    ts = datetime.utcnow().isoformat()
    write_text(CRON_LOG, f"heartbeat {ts}")
