"""
app.py
------
AI Study Coach - FastAPI backend.

Wraps the Google Gemini API and exposes one endpoint that builds a
prompt (zero-shot / few-shot / structured-reasoning) from student
info and sends it to Gemini, returning the generated study plan.

Setup:
    pip install -r requirements.txt
    export GEMINI_API_KEY="your-key-here"   (Windows: set GEMINI_API_KEY=...)
    uvicorn app:app --reload

Then open http://127.0.0.1:8000 in your browser.
"""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from prompts import (
    build_zero_shot_prompt,
    build_few_shot_prompt,
    build_structured_prompt,
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

_model = None
if GEMINI_API_KEY:
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    _model = genai.GenerativeModel(GEMINI_MODEL_NAME)

app = FastAPI(title="AI Study Coach")

TECHNIQUE_BUILDERS = {
    "zero_shot": build_zero_shot_prompt,
    "few_shot": build_few_shot_prompt,
    "structured": build_structured_prompt,
}


class StudentInfo(BaseModel):
    name: str
    subject: str
    weak_topics: str
    days_remaining: int = Field(gt=0, le=60)
    hours_per_day: float = Field(gt=0, le=24)
    skill_level: str
    technique: str  # "zero_shot" | "few_shot" | "structured"


@app.post("/api/generate-plan")
def generate_plan(info: StudentInfo):
    builder = TECHNIQUE_BUILDERS.get(info.technique)
    if builder is None:
        return {"error": f"Unknown technique '{info.technique}'."}

    prompt = builder(info)

    if _model is None:
        return {
            "error": (
                "GEMINI_API_KEY is not set on the server. Set it as an "
                "environment variable and restart the app to get real "
                "responses from Gemini."
            ),
            "prompt_used": prompt,
        }

    try:
        response = _model.generate_content(prompt)
        return {
            "technique": info.technique,
            "prompt_used": prompt,
            "response": response.text,
        }
    except Exception as exc:  # noqa: BLE001 - surface any Gemini/API error to UI
        return {"error": str(exc), "prompt_used": prompt}


# Serve the frontend last, so /api routes above take priority.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
