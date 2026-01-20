"""
Evaluation Agent - Pydantic AI Implementation.
Evaluates interview answers and provides feedback using pydantic-ai with OpenRouter.
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic_ai import Agent
from schemas.evaluation import QuestionAnswerPair, InterviewFeedback

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")

# Define the Pydantic AI agent for answer evaluation
evaluation_agent = Agent(
    model="openrouter/nvidia/nemotron-3-nano-30b-a3b:free",
    api_key=OPENROUTER_API_KEY,
    system_prompt="""You are an expert technical interviewer evaluating software engineering interview answers.
Your task is to provide comprehensive, constructive feedback on candidate responses.

When evaluating answers:
1. Score each answer from 0-10 based on correctness, completeness, and clarity
2. Provide specific, actionable feedback for each answer
3. Identify key strengths across all answers
4. Identify areas for improvement
5. Give an overall readiness summary (2-3 sentences)

Scoring guidelines:
- 0-3: Incorrect or very poor answer
- 4-6: Partially correct, missing key points
- 7-8: Good answer with minor gaps
- 9-10: Excellent, comprehensive answer

Be encouraging but honest and specific.""",
)


def evaluate_answers(qa_pairs: List[QuestionAnswerPair]) -> InterviewFeedback:
    """
    Evaluate interview answers and provide detailed feedback using Pydantic AI.
    
    Args:
        qa_pairs: List of question-answer pairs to evaluate
        
    Returns:
        InterviewFeedback: Comprehensive evaluation with scores, feedback, and summary
        
    Raises:
        Exception: If evaluation fails after retries
    """
    if not qa_pairs or len(qa_pairs) == 0:
        raise ValueError("At least one question-answer pair must be provided")
    
    # Format the Q&A pairs for the prompt
    qa_text = ""
    for i, pair in enumerate(qa_pairs, 1):
        qa_text += f"\nQuestion {i}: {pair.question}\n"
        qa_text += f"Answer {i}: {pair.answer}\n"
    
    max_retries = 1
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            # Use pydantic-ai to run the agent
            result = evaluation_agent.run_sync(
                user_prompt=f"""Evaluate the following question-answer pairs from a technical interview:
{qa_text}

Provide:
1. Individual scores and feedback for each answer (0-10 scale)
2. List of 3-5 key strengths demonstrated
3. List of 3-5 areas for improvement
4. Overall readiness summary (2-3 sentences about interview preparation level)

Be specific and constructive in your feedback.""",
                result_type=InterviewFeedback,
            )
            
            return result.data
            
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                continue
            else:
                raise Exception(f"Answer evaluation failed after {max_retries + 1} attempts: {str(last_error)}")
