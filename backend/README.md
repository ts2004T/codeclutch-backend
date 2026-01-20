# CodeClutch Backend

**AI-powered interview preparation using Pydantic AI & FastAPI**

AI-powered interview preparation platform for Software Engineering roles, designed for college students.

## Overview

CodeClutch is a FastAPI-based backend that leverages **Pydantic AI** and OpenRouter LLM to help students prepare for technical interviews. It features a **multi-agent system** that:

1. **Analyzes resumes** using ResumeAnalysisAgent (Pydantic AI)
2. **Generates interview questions** using QuestionGenerationAgent (Pydantic AI)
3. **Evaluates answers** using AnswerEvaluationAgent (Pydantic AI)

All agent responses are **fully type-safe** with Pydantic schema validation.

## Features

- ✅ **Resume Analysis**: Upload resume (text or PDF) to extract skills, projects, and experience level
- ✅ **Question Generation**: Generate 5 targeted interview questions based on candidate's skills
- ✅ **Answer Evaluation**: Get detailed feedback on interview answers with scores (0-10) and improvement suggestions
- ✅ **Robust Error Handling**: Try/except with 1 automatic retry on LLM failures
- ✅ **Production-Ready**: Deployed on Render with environment variable support
- ✅ **Type-Safe**: All responses validated with Pydantic schemas

## Project Structure

```
backend/
├── main.py                  # FastAPI app & endpoints with error handling
├── agents/                  # Pydantic AI agents (type-safe LLM integration)
│   ├── resume_agent.py      # ResumeAnalysisAgent
│   ├── question_agent.py    # QuestionGenerationAgent
│   └── evaluation_agent.py  # AnswerEvaluationAgent
├── schemas/                 # Pydantic models (strict output validation)
│   ├── resume.py            # ResumeAnalysis model
│   ├── questions.py         # QuestionSet model
│   └── evaluation.py        # InterviewFeedback model
├── utils/
│   └── pdf_parser.py        # PDF text extraction utility
├── requirements.txt         # Python dependencies (includes pydantic-ai)
├── runtime.txt              # Python version (3.11)
├── .env.example             # Environment template
└── Procfile                 # Render deployment config
```

## Architecture: Pydantic AI Agents

Each agent is built with **Pydantic AI** for type-safe LLM integration:

### 1. ResumeAnalysisAgent

- **Model**: nvidia/nemotron-3-nano-30b-a3b:free
- **Input**: Resume text
- **Output Schema**: `ResumeAnalysis` (name, skills, projects, experience_level)
- **Error Handling**: Automatic retry on failure

### 2. QuestionGenerationAgent

- **Model**: nvidia/nemotron-3-nano-30b-a3b:free
- **Input**: List of skills
- **Output Schema**: `QuestionSet` (5 questions with difficulty & skill focus)
- **Error Handling**: Automatic retry on failure

### 3. AnswerEvaluationAgent

- **Model**: nvidia/nemotron-3-nano-30b-a3b:free
- **Input**: Question-answer pairs
- **Output Schema**: `InterviewFeedback` (scores, feedback, strengths, improvements)
- **Error Handling**: Automatic retry on failure

## Why Pydantic AI?

✅ **Type-Safe**: All LLM outputs guaranteed to match Pydantic schemas  
✅ **Validated**: Automatic validation of agent responses  
✅ **Reliable**: Built-in error handling and retry logic  
✅ **Production-Ready**: Works seamlessly with FastAPI  
✅ **Cost-Effective**: Compatible with free OpenRouter LLM models

## Setup

1. **Clone and navigate to project**

   ```bash
   cd codeclutch-backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your **free OpenRouter API key** from https://openrouter.ai/keys:

   ```
   OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
   ```

   The free model used is: `nvidia/nemotron-3-nano-30b-a3b:free`

5. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

   Or:

   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

**API Documentation** (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

### 1. Analyze Resume (Text)

**POST** `/analyze-resume`

Analyze resume text and extract key information.

**Request Body:**

```json
{
  "resume_text": "John Doe\nSoftware Engineer\nSkills: Python, React, Node.js..."
}
```

**Response:**

```json
{
  "name": "John Doe",
  "skills": ["Python", "React", "Node.js"],
  "projects": ["E-commerce Platform", "Chat Application"],
  "experience_level": "intermediate"
}
```

### 2. Analyze Resume (PDF)

**POST** `/analyze-resume-pdf`

Upload PDF resume for analysis.

**Request:** Multipart form-data with PDF file

**Response:** Same as text analysis

### 3. Generate Questions

**POST** `/generate-questions`

Generate interview questions based on skills.

**Request Body:**

```json
{
  "skills": ["Python", "React", "Node.js"]
}
```

**Response:**

```json
{
  "questions": [
    {
      "question": "Explain Python's GIL and its impact on multi-threading",
      "difficulty": "medium",
      "skill_focus": "Python"
    },
    ...
  ]
}
```

### 4. Evaluate Answers

**POST** `/evaluate-answers`

Evaluate interview answers and get feedback.

**Request Body:**

```json
{
  "qa_pairs": [
    {
      "question": "What is React's virtual DOM?",
      "answer": "The virtual DOM is a lightweight copy..."
    }
  ]
}
```

**Response:**

```json
{
  "evaluations": [
    {
      "question": "What is React's virtual DOM?",
      "score": 8,
      "feedback": "Good explanation covering key concepts..."
    }
  ],
  "strengths": ["Clear explanations", "Good technical depth"],
  "improvements": ["Add more real-world examples"],
  "overall_readiness_summary": "Strong candidate with solid fundamentals..."
}
```

## API Documentation

Once running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Technology Stack

- **FastAPI**: Modern web framework
- **Pydantic**: Data validation using Python type hints
- **OpenRouter**: LLM API gateway (using Llama 3.1 8B)
- **PyPDF2**: PDF text extraction

## Design Principles

- **Type Safety**: Strict Pydantic models for all inputs/outputs
- **Clean Code**: Interview-quality, readable code
- **No Overengineering**: Simple, focused implementation
- **Error Handling**: Basic error handling on all endpoints

## Notes

- No authentication implemented (as per requirements)
- No database (in-memory processing only)
- Designed for educational/interview purposes
- LLM responses are parsed using `model_validate_json()` for type safety

## Getting OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Generate an API key from your dashboard
4. Add credits to your account (pay-per-use pricing)

## Development

For development with auto-reload:

```bash
uvicorn main:app --reload --port 8000
```

## License

MIT
