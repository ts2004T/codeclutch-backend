"""
Question Generator Agent - Pydantic AI Implementation.
Generates interview questions based on candidate skills using pydantic-ai with OpenRouter.
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic_ai import Agent
from schemas.questions import QuestionSet

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")

# Define the Pydantic AI agent for question generation
question_generation_agent = Agent(
    model="openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
    api_key=OPENROUTER_API_KEY,
    system_prompt="""You are an expert technical interviewer creating interview questions.
Your task is to generate relevant, practical interview questions for software engineers based on their skills.

When generating questions:
1. Create questions that are specific to the provided skills
2. Include a mix of difficulty levels: 2 basic, 2 medium, 1 hard
3. Ensure at least one question is a deep dive question
4. Focus on practical, real-world scenarios
5. Make questions appropriate for technical interviews

Return exactly 5 questions with clear difficulty levels and skill focus.""",
)


def generate_questions(skills: List[str]) -> QuestionSet:
    """
    Generate interview questions based on candidate's skills using Pydantic AI.
    
    Args:
        skills: List of technical skills extracted from resume
        
    Returns:
        QuestionSet: Set of 5 interview questions with varying difficulty levels
        
    Raises:
        Exception: If generation fails after retries
    """
    if not skills or len(skills) == 0:
        raise ValueError("At least one skill must be provided")
    
    skills_text = ", ".join(skills)
    max_retries = 1
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            # Use pydantic-ai to run the agent
            result = question_generation_agent.run_sync(
                user_prompt=f"""Generate exactly 5 interview questions for a candidate with these skills: {skills_text}

Requirements:
- 2 basic questions (fundamental concepts)
- 2 medium questions (practical application)
- 1 hard question (complex problem-solving)
- Include 1 deep_dive question that explores a topic thoroughly

Make questions specific to the skills provided and practical for real interviews.""",
                result_type=QuestionSet,
            )
            
            return result.data
            
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                continue
            else:
                raise Exception(f"Question generation failed after {max_retries + 1} attempts: {str(last_error)}")
