from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from modules.encryption import FileEncryption
from modules.hashing import sha256_bytes
from modules.blockchain import BlockchainHashSubmitter
import io
import os

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
KEY_PATH = DATA_DIR / "fernet.key"
DATA_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB demo limit
codec = FileEncryption(KEY_PATH)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/status")
def status():
    return jsonify({
        "app": "CipherTrail",
        "encryption": "ready",
        "hashing": "ready",
        "blockchain_configured": bool(os.getenv("BLOCKCHAIN_URL") and os.getenv("BLOCKCHAIN_PRIVATE_KEY")),
        "max_upload_mb": 10,
    })

@app.post("/api/encrypt-text")
def encrypt_text():
    body = request.get_json(silent=True) or {}
    text = body.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Enter some sample text first."}), 400
    encrypted = codec.encrypt_bytes(text.encode("utf-8"))
    return jsonify({
        "encrypted": encrypted.decode("ascii"),
        "sha256": sha256_bytes(encrypted),
        "message": "Text encrypted successfully.",
    })

@app.post("/api/decrypt-text")
def decrypt_text():
    body = request.get_json(silent=True) or {}
    encrypted = body.get("encrypted", "")
    if not isinstance(encrypted, str) or not encrypted.strip():
        return jsonify({"error": "Paste the encrypted text first."}), 400
    try:
        plaintext = codec.decrypt_bytes(encrypted.encode("ascii")).decode("utf-8")
    except Exception:
        return jsonify({"error": "Could not decrypt this text. Check the key and input."}), 400
    return jsonify({"decrypted": plaintext})

@app.post("/api/encrypt-file")
def encrypt_file():
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        return jsonify({"error": "Choose a file first."}), 400
    safe_name = secure_filename(upload.filename) or "uploaded-file"
    raw = upload.read()
    if not raw:
        return jsonify({"error": "The selected file is empty."}), 400
    encrypted = codec.encrypt_bytes(raw)
    digest = sha256_bytes(encrypted)
    return send_file(
        io.BytesIO(encrypted),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=f"{safe_name}.enc",
        headers={"X-Content-SHA256": digest},
    )

@app.post("/api/hash-file")
def hash_file():
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        return jsonify({"error": "Choose a file first."}), 400
    raw = upload.read()
    return jsonify({
        "filename": secure_filename(upload.filename) or "uploaded-file",
        "size_bytes": len(raw),
        "sha256": sha256_bytes(raw),
        "message": "Fingerprint calculated locally by the backend.",
    })

@app.post("/api/anchor-hash")
def anchor_hash():
    body = request.get_json(silent=True) or {}
    digest = body.get("sha256", "")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
        return jsonify({"error": "Provide a valid 64-character SHA-256 digest."}), 400
    submitter = BlockchainHashSubmitter.from_environment()
    tx = submitter.submit_hash(digest)
    if not tx:
        return jsonify({"error": "Blockchain unavailable or not configured. Set up a local development chain and .env first."}), 503
    return jsonify({"transaction": tx, "message": "Hash anchored to the configured development chain."})

@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "File is larger than the 10 MB demo limit."}), 413

if __name__ == "__main__":
    # Local-only bind; do not expose this development server to a public network.
    app.run(host="127.0.0.1", port=5000, debug=False)
