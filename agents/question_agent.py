"""
Question Generator Agent.
Generates interview questions based on candidate skills using LLM.
"""
import os
import requests
from typing import List
from dotenv import load_dotenv
from schemas.questions import QuestionSet

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_questions(skills: List[str]) -> QuestionSet:
    """
    Generate interview questions based on candidate's skills.
    
    Args:
        skills: List of technical skills extracted from resume
        
    Returns:
        QuestionSet: Set of 5 interview questions
        
    Raises:
        Exception: If LLM call or parsing fails
    """
    # Join skills into a readable format
    skills_text = ", ".join(skills)
    
    # Construct the prompt
    prompt = f"""You are an interview question generator for software engineering roles. Generate exactly 5 interview questions based on these skills: {skills_text}

Requirements:
- 2 basic questions
- 2 medium questions  
- 1 hard question
- Include 1 deep_dive question (can overlap with difficulty levels)

Return ONLY valid JSON matching this exact structure (no markdown, no extra text):
{{
    "questions": [
        {{
            "question": "question text here",
            "difficulty": "basic" or "medium" or "hard" or "deep_dive",
            "skill_focus": "the specific skill this question tests"
        }},
        ...5 questions total...
    ]
}}

Make questions specific to the skills provided. Ensure questions are practical and interview-appropriate.
Return ONLY the JSON, nothing else."""

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
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
        question_set = QuestionSet.model_validate_json(llm_output)
        return question_set
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {str(e)}")
