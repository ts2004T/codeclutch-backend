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
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyze resume and extract structured information.
    """

    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY is not set")

    if not resume_text or not resume_text.strip():
        raise Exception("Resume text is empty")

    # Prompt
    prompt = f"""You are a resume analyzer for software engineering roles.

Resume:
{resume_text}

Return ONLY valid JSON matching this structure (no markdown, no extra text):
{{
  "name": "candidate's full name",
  "skills": ["skill1", "skill2"],
  "projects": ["project1", "project2"],
  "experience_level": "beginner" | "intermediate" | "advanced"
}}
"""

    # REQUIRED OpenRouter headers
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://codeclutch-backend.onrender.com",
        "X-Title": "CodeClutch",
    }

    payload = {
        "model": "openchat/openchat-7b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        data = response.json()
        llm_output = data["choices"][0]["message"]["content"].strip()

        return ResumeAnalysis.model_validate_json(llm_output)

    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {e}")
    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {e}")
