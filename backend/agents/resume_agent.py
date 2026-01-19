"""
Resume Analyzer Agent.
Analyzes resume text and extracts key information using LLM.
"""

import os
import requests
from dotenv import load_dotenv
from schemas.resume import ResumeAnalysis

# Load env vars (Render + local)
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyze resume and extract structured information using OpenRouter.
    """

    prompt = f"""
You are a resume analyzer for software engineering roles.

Analyze the resume below and return ONLY valid JSON in this format:

{{
  "name": "candidate name or Unknown",
  "skills": ["skill1", "skill2"],
  "projects": ["project 1", "project 2"],
  "experience_level": "beginner" | "intermediate" | "advanced"
}}

Resume:
{resume_text}

Return ONLY JSON. No markdown. No explanation.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codeclutch-backend.onrender.com",
        "X-Title": "CodeClutch"
    }

    payload = {
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]

        return ResumeAnalysis.model_validate_json(content)

    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {e}")
    except Exception as e:
        raise Exception(f"Failed to parse model output: {e}")
