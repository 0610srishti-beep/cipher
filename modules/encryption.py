from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FileEncryption:
    """Fernet encryption helper for files and user-provided demo text."""
    def __init__(self, key_file: Path):
        self.key_file = Path(key_file)
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
        self.cipher = Fernet(key)

    def encrypt_bytes(self, content: bytes) -> bytes:
        return self.cipher.encrypt(content)

    def decrypt_bytes(self, content: bytes) -> bytes:
        return self.cipher.decrypt(content)

    def encrypt_file(self, source: Path, destination: Path) -> None:
        Path(destination).write_bytes(self.encrypt_bytes(Path(source).read_bytes()))

    def decrypt_file(self, source: Path, destination: Path) -> None:
        Path(destination).write_bytes(self.decrypt_bytes(Path(source).read_bytes()))
