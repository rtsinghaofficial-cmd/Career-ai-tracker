# Career System — FastAPI + HTML

## Stack
- **Backend:** Python + FastAPI (REST API)
- **Frontend:** Plain HTML/CSS/JS (no framework)
- **AI:** Anthropic Claude API for skill extraction

## Project Structure
```
career-app-python/
├── main.py           ← FastAPI backend (all API routes)
├── requirements.txt  ← Python dependencies
├── README.md
└── static/
    └── index.html    ← Full frontend (HTML + CSS + JS)
```

## Setup

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows
set ANTHROPIC_API_KEY=sk-ant-...
```
Get your key from: https://console.anthropic.com

### 4. Run the server
```bash
uvicorn main:app --reload
```
Open http://localhost:8000 in your browser.

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/jobs | List all jobs |
| POST | /api/jobs | Add a job |
| DELETE | /api/jobs/{id} | Delete a job |
| GET | /api/skills | List all skills |
| POST | /api/skills | Add a skill |
| PATCH | /api/skills/{id} | Update skill bucket |
| DELETE | /api/skills/{id} | Delete a skill |
| GET | /api/reviews | List weekly reviews |
| POST | /api/reviews | Add a review |
| POST | /api/extract-skills | AI skill extraction |

## Notes
- Data is stored in-memory and resets on server restart
- To persist data, replace the `db` dict in `main.py` with SQLite using SQLAlchemy
