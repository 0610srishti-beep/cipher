from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
KEY_FILE = DATA_DIR / "fernet.key"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
