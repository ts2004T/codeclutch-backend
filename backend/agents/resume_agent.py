"""
Resume Analyzer Agent - Pydantic AI Implementation.
Analyzes resume text and extracts key information using pydantic-ai with OpenRouter.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from schemas.resume import ResumeAnalysis

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")

# Define the Pydantic AI agent for resume analysis
resume_analysis_agent = Agent(
    model="openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
    api_key=OPENROUTER_API_KEY,
    system_prompt="""You are an expert resume analyzer for software engineering roles.
Your task is to extract key information from resumes and classify candidates.

When analyzing a resume:
1. Extract the candidate's name (or return "Unknown" if not found)
2. Identify all technical skills (programming languages, frameworks, tools)
3. List significant projects (at least 2-3 if available)
4. Classify experience level based on years and complexity

Be thorough but concise. Return structured data only.""",
)


def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """
    Analyze resume and extract structured information using Pydantic AI.
    
    Args:
        resume_text: The resume text to analyze
        
    Returns:
        ResumeAnalysis: Structured analysis with name, skills, projects, and experience level
        
    Raises:
        Exception: If analysis fails after retries
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty")
    
    max_retries = 1
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            # Use pydantic-ai to run the agent
            result = resume_analysis_agent.run_sync(
                user_prompt=f"""Analyze this resume and extract key information:

{resume_text}

Return the analysis as structured data.""",
                result_type=ResumeAnalysis,
            )
            
            return result.data
            
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                continue
            else:
                raise Exception(f"Resume analysis failed after {max_retries + 1} attempts: {str(last_error)}")
