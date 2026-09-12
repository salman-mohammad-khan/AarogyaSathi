# AarogyaSathi Team Collaboration & Contributing Guide

Welcome to the **AarogyaSathi (आरोग्यसाथी)** development team! This guide outlines our Git workflow, coding standards, branch conventions, and review processes to ensure smooth teamwork.

---

## 🚀 Quickstart for Team Members

### 1. Clone the Repository
```bash
git clone https://github.com/salman-mohammad-khan/AarogyaSathi.git
cd AarogyaSathi
```

### 2. Set Up Python Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Open `.env` and fill in your keys (e.g. `OLLAMA_API_KEY`, `GOOGLE_FACTCHECK_API_KEY`).  
> ⚠️ **NEVER commit or push `.env` to GitHub.**

### 5. Download ML Models (One-Time Setup)
```bash
python scripts/setup.py
```

### 6. Run the App Locally
```bash
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000) to test the web interface.

---

## 🌿 Git & Branching Strategy

We follow the **GitHub Flow** with feature branches. **Nobody pushes directly to `main`**.

```
main (always stable & deployable to Oracle Cloud VM)
  │
  ├── feature/whatsapp-webhook      (Teammate A)
  ├── feature/pincode-directory     (Teammate B)
  └── fix/symptom-negation          (Teammate C)
```

### Branch Naming Convention
Use descriptive branch names with appropriate prefixes:
- `feature/<name>` : New features or endpoints (e.g., `feature/whatsapp-cloud-api`, `feature/ui-dark-mode`)
- `fix/<name>`     : Bug fixes (e.g., `fix/fasttext-crash`, `fix/outbreak-rss-timeout`)
- `docs/<name>`    : Documentation updates (e.g., `docs/api-specs`, `docs/setup-guide`)
- `test/<name>`    : Adding or updating unit tests (e.g., `test/intent-eval`)
- `refactor/<name>`: Code restructuring without feature changes

### Daily Workflow

1. **Pull the latest changes from `main`**:
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Create your feature branch**:
   ```bash
   git checkout -b feature/my-feature-name
   ```
3. **Make your changes, test locally**:
   ```bash
   pytest tests/
   ```
4. **Commit with descriptive messages** (use conventional commits):
   ```bash
   git add .
   git commit -m "feat(whatsapp): implement Meta Cloud API webhook verification"
   ```
5. **Push your branch to GitHub**:
   ```bash
   git push -u origin feature/my-feature-name
   ```
6. **Open a Pull Request (PR)** on GitHub:
   - Provide a brief summary of your changes.
   - Request review from at least one teammate.
   - Ensure tests pass before merging.

---

## 📝 Commit Message Guidelines

Use clear, structured commit messages:
- `feat: ...` for new features or capabilities.
- `fix: ...` for bug fixes.
- `docs: ...` for documentation changes.
- `style: ...` for formatting or CSS changes.
- `refactor: ...` for code cleanups that don't alter functionality.
- `test: ...` for adding or improving test coverage.

---

## 🧪 Testing Before Pull Request

Always verify your changes before opening a PR:
```bash
# Run test suite
pytest tests/

# Run benchmark / accuracy eval
python scripts/eval.py
```

---

## 🛡️ Production Deployment (Oracle Cloud VM)

The production VM (`130.210.56.87`) runs the code from the `main` branch.  
Only code that has been reviewed, tested, and merged into `main` should be deployed to the VM.
