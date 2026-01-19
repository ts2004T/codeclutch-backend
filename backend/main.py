"""
CodeClutch - AI-Powered Interview Preparation Backend

FastAPI application providing endpoints for resume analysis,
question generation, and answer evaluation for software engineering interviews.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

# Import schemas
from schemas.resume import ResumeAnalysis
from schemas.questions import QuestionSet
from schemas.evaluation import QuestionAnswerPair, InterviewFeedback

# Import agents
from agents.resume_agent import analyze_resume
from agents.question_agent import generate_questions
from agents.evaluation_agent import evaluate_answers

# Import utilities
from utils.pdf_parser import extract_text_from_pdf, clean_resume_text

# Initialize FastAPI app
app = FastAPI(
    title="CodeClutch API",
    description="AI-powered interview preparation for software engineers",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models for endpoints

class ResumeTextInput(BaseModel):
    """Input schema for text-based resume analysis"""
    resume_text: str


class QuestionGenerationInput(BaseModel):
    """Input schema for question generation"""
    skills: List[str]


class AnswerEvaluationInput(BaseModel):
    """Input schema for answer evaluation"""
    qa_pairs: List[QuestionAnswerPair]


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "CodeClutch API is running",
        "version": "1.0.0",
        "status": "active"
    }


@app.post("/analyze-resume", response_model=ResumeAnalysis)
async def analyze_resume_endpoint(input_data: ResumeTextInput):
    """
    Analyze a resume and extract key information.
    
    Args:
        input_data: ResumeTextInput containing resume text
        
    Returns:
        ResumeAnalysis: Extracted information including name, skills, projects, and experience level
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Clean the resume text
        cleaned_text = clean_resume_text(input_data.resume_text)
        
        # Call the resume agent
        analysis = analyze_resume(cleaned_text)
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {str(e)}"
        )


@app.post("/analyze-resume-pdf", response_model=ResumeAnalysis)
async def analyze_resume_pdf_endpoint(file: UploadFile = File(...)):
    """
    Analyze a PDF resume and extract key information.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        ResumeAnalysis: Extracted information including name, skills, projects, and experience level
        
    Raises:
        HTTPException: If PDF parsing or analysis fails
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Read PDF bytes
        pdf_bytes = await file.read()
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(pdf_bytes)
        cleaned_text = clean_resume_text(resume_text)
        
        # Call the resume agent
        analysis = analyze_resume(cleaned_text)
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF resume analysis failed: {str(e)}"
        )


@app.post("/generate-questions", response_model=QuestionSet)
async def generate_questions_endpoint(input_data: QuestionGenerationInput):
    """
    Generate interview questions based on candidate skills.
    
    Args:
        input_data: QuestionGenerationInput containing list of skills
        
    Returns:
        QuestionSet: Set of 5 interview questions with varying difficulty
        
    Raises:
        HTTPException: If question generation fails
    """
    try:
        # Validate input
        if not input_data.skills:
            raise HTTPException(
                status_code=400,
                detail="Skills list cannot be empty"
            )
        
        # Call the question agent
        questions = generate_questions(input_data.skills)
        return questions
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question generation failed: {str(e)}"
        )


@app.post("/evaluate-answers", response_model=InterviewFeedback)
async def evaluate_answers_endpoint(input_data: AnswerEvaluationInput):
    """
    Evaluate interview answers and provide feedback.
    
    Args:
        input_data: AnswerEvaluationInput containing question-answer pairs
        
    Returns:
        InterviewFeedback: Detailed feedback with scores, strengths, and improvements
        
    Raises:
        HTTPException: If evaluation fails
    """
    try:
        # Validate input
        if not input_data.qa_pairs:
            raise HTTPException(
                status_code=400,
                detail="Question-answer pairs list cannot be empty"
            )
        
        # Call the evaluation agent
        feedback = evaluate_answers(input_data.qa_pairs)
        return feedback
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Answer evaluation failed: {str(e)}"
        )


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
