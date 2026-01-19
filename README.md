# CodeClutch Backend

AI-powered interview preparation platform for Software Engineering roles, designed for college students.

## Overview

CodeClutch is a FastAPI-based backend that leverages AI to help students prepare for technical interviews. It analyzes resumes, generates relevant interview questions, and evaluates answers with detailed feedback.

## Features

- **Resume Analysis**: Upload resume (text or PDF) to extract skills, projects, and experience level
- **Question Generation**: Generate 5 targeted interview questions based on candidate's skills
- **Answer Evaluation**: Get detailed feedback on interview answers with scores (0-10) and improvement suggestions

## Project Structure

```
codeclutch-backend/
├── main.py                  # FastAPI application with endpoints
├── agents/
│   ├── resume_agent.py      # Resume analysis agent
│   ├── question_agent.py    # Question generation agent
│   └── evaluation_agent.py  # Answer evaluation agent
├── schemas/
│   ├── resume.py            # Pydantic models for resume data
│   ├── questions.py         # Pydantic models for questions
│   └── evaluation.py        # Pydantic models for evaluation
├── utils/
│   └── pdf_parser.py        # PDF text extraction utility
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

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

   Edit `.env` and add your OpenRouter API key:

   ```
   OPENROUTER_API_KEY=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
   ```

5. **Run the application**

   ```bash
   python main.py
   ```

   Or with uvicorn directly:

   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

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
