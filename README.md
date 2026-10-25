# CipherTrail — Secure File Audit Dashboard

CipherTrail is a small, student-friendly cybersecurity demo with a dark dashboard. It lets a user enter sample text or choose a local file, encrypt it, inspect its SHA-256 fingerprint, and optionally anchor that fingerprint to a local Ethereum-compatible development chain.

The interface is intentionally simple: the goal is to make the security workflow easy to follow during a class demo, not to pretend that a student prototype is a production security product.

## Features
- Dark dashboard with a live status summary
- Text encryption and decryption
- File encryption and SHA-256 integrity verification
- Optional blockchain hash anchoring
- Clear separation between frontend and Python backend
- Local-only processing by default

## Safety and privacy
This project does **not** capture system-wide keystrokes, monitor other applications, or run hidden background surveillance. Users must explicitly provide text or select a file for processing. The browser sends selected file contents only to the local Flask server at `127.0.0.1`.

Blockchain submission is optional. Use only a disposable development account on a local test chain. Never put a real wallet key into the app or commit `.env`.

## Stack
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python + Flask
- Encryption: Fernet (`cryptography`)
- Hashing: SHA-256
- Optional blockchain: Web3.py

## Windows setup
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe app.py
```
Open the local URL printed in the terminal (usually `http://127.0.0.1:5000`).

## Run tests
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## GitHub
Create a new empty repository on GitHub, then run from this folder:
```powershell
git init
git add .
git commit -m "Build CipherTrail security dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

## Notes
- The Fernet key is generated locally in `data/fernet.key` and excluded from Git.
- Uploaded/processed files and generated keys stay in the local `data/` directory.
- Blockchain features remain unavailable until `BLOCKCHAIN_URL` and `BLOCKCHAIN_PRIVATE_KEY` are set in `.env`.
- This is an educational prototype; review and harden it before using it with sensitive files.
