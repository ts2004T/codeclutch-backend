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

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://codeclutch-backend.onrender.com",
    "X-Title": "CodeClutch"
}


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyze resume and extract structured information.
    
    Args:
        resume_text: The text content of the resume
        
    Returns:
        ResumeAnalysis: Structured resume information
        
    Raises:
        Exception: If LLM call or parsing fails
    """
    # Construct the prompt
    prompt = f"""You are a resume analyzer for software engineering roles. Analyze the following resume and extract key information.

Resume:
{resume_text}

Return ONLY valid JSON matching this exact structure (no markdown, no extra text):
{{
    "name": "candidate's full name",
    "skills": ["skill1", "skill2", ...],
    "projects": ["project1", "project2", ...],
    "experience_level": "beginner" or "intermediate" or "advanced"
}}

Experience level guidelines:
- beginner: Students, recent grads, < 1 year experience
- intermediate: 1-3 years experience, internships
- advanced: 3+ years, multiple projects, leadership

Extract all technical skills mentioned. List all projects with brief descriptions.
Return ONLY the JSON, nothing else."""

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openchat/openchat-7b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        # Extract the response text
        response_data = response.json()
        llm_output = response_data["choices"][0]["message"]["content"].strip()
        
        # Parse using Pydantic
        analysis = ResumeAnalysis.model_validate_json(llm_output)
        return analysis
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {str(e)}")
