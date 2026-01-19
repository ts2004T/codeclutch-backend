"""
Pydantic schemas for answer evaluation.
"""
from pydantic import BaseModel, Field
from typing import List


class QuestionAnswerPair(BaseModel):
    """
    Input schema for evaluation agent.
    Represents a question and its answer.
    """
    question: str
    answer: str


class AnswerEvaluation(BaseModel):
    """
    Evaluation for a single question-answer pair.
    """
    question: str
    score: int = Field(..., ge=0, le=10, description="Score from 0 to 10")
    feedback: str


class InterviewFeedback(BaseModel):
    """
    Output schema for evaluation agent.
    Contains overall feedback and individual evaluations.
    """
    evaluations: List[AnswerEvaluation]
    strengths: List[str]
    improvements: List[str]
    overall_readiness_summary: str
