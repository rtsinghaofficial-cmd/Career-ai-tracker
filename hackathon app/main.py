from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import anthropic
import json
import os

app = FastAPI()

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ── In-memory store (resets on restart) ──────────────────────────────────────
db = {
    "jobs": [],
    "skills": [],
    "reviews": [],
}

# ── Models ────────────────────────────────────────────────────────────────────
class Job(BaseModel):
    id: int | None = None
    title: str
    company: str = ""
    skills: list[str] = []
    notes: str = ""
    date: str = ""

class Skill(BaseModel):
    id: int | None = None
    name: str
    bucket: str = "❌ Backlog"

class Review(BaseModel):
    id: int | None = None
    learned: str = ""
    jobsViewed: str = ""
    nextSkill: str = ""
    wins: str = ""
    blockers: str = ""
    date: str = ""

class ExtractRequest(BaseModel):
    job_description: str

# ── Jobs ──────────────────────────────────────────────────────────────────────
@app.get("/api/jobs")
def get_jobs():
    return db["jobs"]

@app.post("/api/jobs")
def add_job(job: Job):
    from datetime import date
    job.id = int(__import__("time").time() * 1000)
    job.date = date.today().strftime("%m/%d/%Y")
    db["jobs"].append(job.dict())
    return job

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int):
    db["jobs"] = [j for j in db["jobs"] if j["id"] != job_id]
    return {"ok": True}

# ── Skills ────────────────────────────────────────────────────────────────────
@app.get("/api/skills")
def get_skills():
    return db["skills"]

@app.post("/api/skills")
def add_skill(skill: Skill):
    if any(s["name"] == skill.name for s in db["skills"]):
        raise HTTPException(400, "Skill already exists")
    skill.id = int(__import__("time").time() * 1000)
    db["skills"].append(skill.dict())
    return skill

@app.patch("/api/skills/{skill_id}")
def update_skill(skill_id: int, updates: dict):
    for s in db["skills"]:
        if s["id"] == skill_id:
            s.update(updates)
            return s
    raise HTTPException(404, "Skill not found")

@app.delete("/api/skills/{skill_id}")
def delete_skill(skill_id: int):
    db["skills"] = [s for s in db["skills"] if s["id"] != skill_id]
    return {"ok": True}

# ── Reviews ───────────────────────────────────────────────────────────────────
@app.get("/api/reviews")
def get_reviews():
    return db["reviews"]

@app.post("/api/reviews")
def add_review(review: Review):
    from datetime import date
    review.id = int(__import__("time").time() * 1000)
    review.date = date.today().strftime("%b %d, %Y")
    db["reviews"].insert(0, review.dict())
    return review

# ── AI Skill Extractor ────────────────────────────────────────────────────────
@app.post("/api/extract-skills")
def extract_skills(req: ExtractRequest):
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": (
                    "Extract the top 8-10 skills from this job description. "
                    "Return ONLY a JSON array of skill name strings, no explanation, "
                    "no markdown, no backticks. Example: [\"Python\",\"SQL\",\"Excel\"]\n\n"
                    f"Job description:\n{req.job_description}"
                )
            }]
        )
        text = message.content[0].text.strip()
        skills = json.loads(text)
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {str(e)}")

# ── Serve frontend ────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
