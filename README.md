
---

# SecretShield 🛡️

*Automated Git-Native Security Auditing & AI Privacy Protection*

---

## 🚀 The Business Value

In modern development, a single leaked credential can result in cloud infrastructure breaches, significant financial loss, and compromised data privacy. **SecretShield** addresses two critical modern threats:

1. **Git-Leak Prevention:** Stopping high-entropy keys from entering version control.
2. **AI-Context Sanitization:** Protecting local configuration files from being accidentally indexed by AI coding assistants (Copilot, Cursor, etc.).

---

## 🏗️ Architecture Overview

SecretShield is built for high-performance security auditing using a modular Python architecture.

### Key Modules:

* **Scanner Engine:** Employs regex pattern matching combined with Shannon Entropy analysis to detect high-risk keys.
* **Git Forensics:** Utilizes `GitPython` to perform deep-tree traversal of commit history to uncover past leaks.
* **Privacy Watcher:** A proactive workspace monitor that identifies sensitive configuration files (`.env`, `.pem`, etc.) prone to accidental AI ingestion.
* **Guard Rail:** An "Shift-Left" security gate that intercepts `git commit` workflows.

---

## 📂 Project Structure

```text
SecretShield/
├── secretshield/           # Core Logic
│   ├── cli.py              # CLI Entry Point (Typer)
│   ├── scanner.py          # Entropy & Regex Engine
│   └── git_utils.py        # Git Staging & History Logic
├── tests/                  # Test Data & Suites
│   ├── test_secret.env     # Simulated sensitive env
│   └── private_key.pem     # Simulated private key
├── Dockerfile              # Containerized deployment
└── README.md

```

---

## 🛠️ Feature Verification

To demonstrate the security pipeline, run these commands:

| Command | Purpose |
| --- | --- |
| `python -m secretshield.cli watch .` | **AI Privacy:** Scans for files that shouldn't be indexed. |
| `python -m secretshield.cli scan tests/` | **Regex Audit:** Deep scan for hardcoded secrets. |
| `git add <file> && python -m secretshield.cli guard` | **Shift-Left Guard:** Block secrets before staging. |
| `python -m secretshield.cli history` | **Forensics:** Deep-scan repository git history. |

---

## ⚙️ Setup & Installation

### Option A: Local Dev

```bash
git clone https://github.com/krsatyam99/Secretshield-ScannerCLI-tool.git
cd SecretShield
pip install -r requirements.txt

```

### Option B: Dockerized Scan

```bash
docker build -t secretshield .
docker run --rm -v $(pwd):/app secretshield watch .

```

---

## 💡 Why SecretShield?

* **Zero-Leak Policy:** Built to ensure secrets never reach the remote repository.
* **Privacy-Centric:** All scanning is performed locally; no data leaves your machine.
* **Developer-First:** Designed to integrate seamlessly into existing terminal-heavy workflows.

*Engineered by a Senior Python Developer with a focus on clean, scalable, and secure architecture.*

---

## 🗺️ Roadmap

* [x] **Core Scanner:** Pattern & Entropy analysis.
* [x] **Git History Forensics:** Deep commit traversal.
* [x] **AI Privacy Watch:** Proactive local file monitoring.
* [x] **Shift-Left Guard:** Staged-file pre-commit protection.
* [ ] **Cloud CI/CD Integration:** Automated GitHub Actions pipeline.

---


