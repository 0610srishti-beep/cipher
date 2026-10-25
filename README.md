# CipherTrail — Secure File Audit Dashboard

CipherTrail is a Python-based cybersecurity project that demonstrates file encryption, data integrity verification, and optional blockchain-based hash recording through a web dashboard. It combines a simple user interface with modular backend components to make core security concepts easier to understand and demonstrate.

## Overview

The project provides a centralized interface for encrypting sample text, processing files, generating SHA-256 fingerprints, and optionally recording file hashes on a local Ethereum-compatible development blockchain.

CipherTrail is designed as an educational prototype for exploring encryption, integrity verification, and blockchain integration. It is not intended to replace production-grade security software.

## Key Features

- **Text Encryption and Decryption:** Protect user-provided text using Fernet symmetric encryption.
- **File Encryption:** Encrypt selected files and download the encrypted output.
- **Integrity Verification:** Generate SHA-256 fingerprints to help identify changes in file contents.
- **Blockchain Integration:** Optionally submit a file hash to a configured local development blockchain.
- **Modular Architecture:** Keep encryption, hashing, blockchain integration, and frontend assets organized into separate components.
- **Web-Based Dashboard:** Access the application's features through a responsive dark-themed interface.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Encryption | Fernet via `cryptography` |
| Hashing | SHA-256 via `hashlib` |
| Blockchain | Web3.py, Ethereum-compatible development chain |
| Testing | Python `unittest` |

## Project Structure

```text
cipher/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── modules/
│   ├── __init__.py
│   ├── encryption.py
│   ├── hashing.py
│   └── blockchain.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── tests/
    └── test_modules.py
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- A modern web browser
- A local Ethereum-compatible development blockchain, only if using the optional blockchain feature

### 1. Clone the Repository

```bash
git clone https://github.com/0610srishti-beep/cipher.git
cd cipher
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -m venv .venv
```

### 3. Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local environment file by copying the example:

```powershell
Copy-Item .env.example .env
```

The blockchain feature is optional. To enable it, configure `BLOCKCHAIN_URL` and `BLOCKCHAIN_PRIVATE_KEY` in `.env` using a disposable development account and a local test chain.

Do not use a personal wallet's private key or commit your `.env` file to version control.

### 5. Run the Application

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the following address in your browser:

**http://127.0.0.1:5000**

Keep the terminal running while you use the dashboard.

## Running Tests

Run the project's unit tests with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests cover encryption/decryption round-trip behavior and SHA-256 hashing.

## Security and Privacy Considerations

- The application processes only text or files explicitly provided by the user.
- It does not capture system-wide keystrokes or monitor other applications.
- File processing is handled by the local Flask server during local use.
- The generated Fernet key is stored locally under `data/fernet.key`.
- The `.gitignore` file excludes local environment settings, generated data, and virtual environment files.
- Blockchain submission records a hash, not the original file contents.
- A SHA-256 fingerprint can help detect content changes, but it does not independently prove who created or authorized a file.
- This project is an educational prototype and requires further security review before any production use.

## Limitations

- The development server is intended for local testing, not production deployment.
- Blockchain functionality requires a reachable, correctly configured development chain and a funded test account.
- Encryption and decryption depend on retaining the correct Fernet key.
- The current implementation does not provide user accounts, role-based access control, or a production key-management system.

## Future Improvements

- Add authenticated user accounts and access controls.
- Introduce secure key-management options.
- Add file verification against previously recorded fingerprints.
- Improve audit history and transaction status reporting.
- Add deployment configuration and automated testing through CI.

## License

No license has been specified for this repository. Unless a license is added, reuse and redistribution are subject to applicable copyright law.

---

**CipherTrail** — Exploring encryption, integrity verification, and blockchain through a modular cybersecurity dashboard.