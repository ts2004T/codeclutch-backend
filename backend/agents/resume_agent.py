"""
Resume Analyzer Agent.
Analyzes resume text and extracts key information using LLM.
"""

import os
import requests
from dotenv import load_dotenv
from schemas.resume import ResumeAnalysis

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

OPENROUTER_URL = "https://openrouter.ai/api/v1/completions"


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyze resume and extract structured information.
    """

    prompt = f"""
You are a resume analyzer for software engineering roles.

Analyze the following resume and return ONLY valid JSON
(no markdown, no extra text) in this exact format:

{{
  "name": "candidate full name or Unknown",
  "skills": ["skill1", "skill2"],
  "projects": ["project1", "project2"],
  "experience_level": "beginner" | "intermediate" | "advanced"
}}

Resume:
{resume_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codeclutch-backend.onrender.com",
        "X-Title": "CodeClutch"
    }

    payload = {
        "model": "openchat/openchat-7b",
        "prompt": prompt,
        "max_tokens": 500,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        llm_output = data["choices"][0]["text"].strip()

        return ResumeAnalysis.model_validate_json(llm_output)

    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {e}")

    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {e}")
