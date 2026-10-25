import hashlib

def sha256_bytes(content: bytes) -> str:
    """Return a stable SHA-256 fingerprint for the given bytes."""
    return hashlib.sha256(content).hexdigest()
