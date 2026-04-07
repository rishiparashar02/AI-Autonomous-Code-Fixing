from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
import os

from main import analyze_bug

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please set it in .env")



class AnalyzeRequest(BaseModel):
    repo_url: str
    bug_description: str
    dest: Optional[str] = "./cloned_repos"
    max_locations: Optional[int] = 5
    apply_fixes: Optional[bool] = False


app = FastAPI(
    title="AI Autonomous Bug Fixing System API",
    description="Expose the bug analysis and patch generation pipeline over HTTP.",
    version="0.1.0",
)

# Allow all origins by default so the API can be called from web frontends.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/analyze-bug")
async def analyze_bug_endpoint(request: AnalyzeRequest):
    """Run the AI analysis pipeline and optionally apply fixes.

    The response includes information about the repository scan, the suggested fixes, and (if apply_fixes=True) the generated git diff.
    """
    try:
        result = analyze_bug(
            repo_url=request.repo_url,
            bug_description=request.bug_description,
            dest=request.dest,
            max_locations=request.max_locations,
            apply_fixes=request.apply_fixes,
        )

        if result is None:
            raise HTTPException(status_code=500, detail="Repository analysis failed (see server logs).")

        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    uvicorn.run("backend.api_server:app", reload=True)
