"""
Evaluation Agent.
Evaluates interview answers and provides feedback using LLM.
"""
import os
import requests
from typing import List
from dotenv import load_dotenv
from schemas.evaluation import QuestionAnswerPair, InterviewFeedback

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def evaluate_answers(qa_pairs: List[QuestionAnswerPair]) -> InterviewFeedback:
    """
    Evaluate interview answers and provide detailed feedback.
    
    Args:
        qa_pairs: List of question-answer pairs to evaluate
        
    Returns:
        InterviewFeedback: Comprehensive evaluation with scores and feedback
        
    Raises:
        Exception: If LLM call or parsing fails
    """
    # Format the Q&A pairs for the prompt
    qa_text = ""
    for i, pair in enumerate(qa_pairs, 1):
        qa_text += f"\nQuestion {i}: {pair.question}\n"
        qa_text += f"Answer {i}: {pair.answer}\n"
    
    # Construct the prompt
    prompt = f"""You are an expert technical interviewer evaluating answers for software engineering interview questions.

Evaluate the following question-answer pairs:
{qa_text}

Return ONLY valid JSON matching this exact structure (no markdown, no extra text):
{{
    "evaluations": [
        {{
            "question": "the question text",
            "score": 7,
            "feedback": "detailed feedback for this answer"
        }},
        ...one for each question...
    ],
    "strengths": ["strength1", "strength2", "strength3"],
    "improvements": ["improvement1", "improvement2", "improvement3"],
    "overall_readiness_summary": "2-3 sentence summary of candidate's readiness"
}}

Scoring guidelines (0-10):
- 0-3: Incorrect or very poor answer
- 4-6: Partially correct, missing key points
- 7-8: Good answer with minor gaps
- 9-10: Excellent, comprehensive answer

Provide specific, actionable feedback. Be encouraging but honest.
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
        feedback = InterviewFeedback.model_validate_json(llm_output)
        return feedback
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API call failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to parse LLM response: {str(e)}")
