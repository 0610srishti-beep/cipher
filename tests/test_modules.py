import tempfile
import unittest
from pathlib import Path
from modules.encryption import FileEncryption
from modules.hashing import sha256_bytes

class ModuleTests(unittest.TestCase):
    def test_encrypt_decrypt_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            codec = FileEncryption(Path(temp) / "test.key")
            original = b"student demo text"
            encrypted = codec.encrypt_bytes(original)
            self.assertNotEqual(encrypted, original)
            self.assertEqual(codec.decrypt_bytes(encrypted), original)

    def test_hash_is_sha256_length(self):
        self.assertEqual(len(sha256_bytes(b"sample")), 64)
        self.assertEqual(sha256_bytes(b"sample"), sha256_bytes(b"sample"))
        self.assertNotEqual(sha256_bytes(b"sample"), sha256_bytes(b"changed"))

if __name__ == "__main__":
    unittest.main()
