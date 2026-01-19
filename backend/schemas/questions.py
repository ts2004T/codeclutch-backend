"""
Pydantic schemas for interview questions.
"""
from pydantic import BaseModel
from typing import List
from enum import Enum


class Difficulty(str, Enum):
    """Question difficulty levels"""
    BASIC = "basic"
    MEDIUM = "medium"
    HARD = "hard"
    DEEP_DIVE = "deep_dive"


class InterviewQuestion(BaseModel):
    """
    Schema for a single interview question.
    """
    question: str
    difficulty: Difficulty
    skill_focus: str


class QuestionSet(BaseModel):
    """
    Output schema for question generator agent.
    Contains a set of 5 interview questions.
    """
    questions: List[InterviewQuestion]
