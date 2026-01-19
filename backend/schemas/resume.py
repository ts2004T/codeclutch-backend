"""
Pydantic schemas for resume analysis.
"""
from pydantic import BaseModel
from typing import List
from enum import Enum


class ExperienceLevel(str, Enum):
    """Experience level classification"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ResumeAnalysis(BaseModel):
    """
    Output schema for resume analyzer agent.
    Contains extracted information from the resume.
    """
    name: str
    skills: List[str]
    projects: List[str]
    experience_level: ExperienceLevel
