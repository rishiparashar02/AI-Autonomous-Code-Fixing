# AI Autonomous Bug Fixing System

An intelligent, end-to-end system that analyzes GitHub repositories to detect bug-related code, extract relevant snippets, and optionally apply AI-driven fixes in an automated workflow.

---

## 📁 Project Structure

```
ai-bug-fixer/
├── .venv/                     # Python virtual environment
├── cloned_repos/              # Temporary cloned repositories
├── backend/
│   └── api_server.py          # FastAPI backend server
├── frontend/                  # Frontend application (e.g., Vite/React)
├── main.py                    # CLI entry point
├── services/
│   ├── repo_manager.py        # Handles repository cloning & cleanup
│   ├── file_scanner.py        # Scans and filters source files
│   ├── bug_locator.py         # Identifies bug-relevant files
│   └── snippet_extractor.py   # Extracts contextual code snippets
├── utils/
│   └── logger.py              # Logging utility
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- Automatic GitHub repository cloning  
- Intelligent source file scanning  
- Keyword-based bug localization  
- Context-aware code snippet extraction  
- AI-assisted bug fixing (optional)  
- Automatic branch creation for fixes  
- Test execution (if available)  
- Summary report generation  

---

## ⚙️ Prerequisites

- Python 3.x  
- Node.js & npm  
- Git (added to system PATH)  

---

## 🧰 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ai-bug-fixer
```

### 2. Setup Python Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**Mac/Linux**
```bash
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## ▶️ Running the Application

### 🔹 Run Backend (FastAPI)

```bash
python -m uvicorn backend.api_server:app --reload
```

- Default: http://127.0.0.1:8000  

---

### 🔹 Run Frontend

```bash
npm run dev
```

- Default: http://localhost:5173  

---

### 🔹 Run via CLI

```bash
python main.py <repo_url> "<bug_description>" [--dest <destination>]
```

#### Example

```bash
python main.py https://github.com/octocat/Hello-World.git "function not working properly"
```

---

## 🔄 System Workflow (Pipeline)

1. **Repository Cloning**
   - Clones repo if not present  

2. **File Scanning**
   - Supports `.py`, `.js`, `.java`  

3. **Bug Localization**
   - Matches keywords with code  

4. **Snippet Extraction**
   - Extracts surrounding code context  

---

## 🌿 Branch & Fix Behavior

- Creates a new branch  
- Applies AI fixes  
- Generates summary README  
- Runs tests (if available)  
- Commits & pushes changes  

---

## 📊 Output

- Total source files  
- Relevant files  
- Extracted snippets  
- File paths + line numbers + code  

---

## 🛠 Troubleshooting

- Git not installed → add to PATH  
- Permission denied → check folder access  
- No snippets → change keywords  
- Invalid URL → verify repo link  
- Network issues → check internet  

Install GitPython if needed:

```bash
pip install gitpython
```

---

## 📦 Dependencies

- GitPython  
- FastAPI / Uvicorn  
- Node.js  

---

## 💡 Future Improvements

- Semantic search (embeddings)  
- Multi-language support  
- Auto PR creation  
- CI/CD integration  
