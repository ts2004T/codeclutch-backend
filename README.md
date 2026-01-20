<<<<<<< HEAD
# CodeClutch – AI-Powered Interview Preparation Platform

> **Transform your interview preparation with AI. Get personalized questions and expert feedback based on your resume and skills.**

---

## 📋 Overview

CodeClutch is a full-stack web application that uses multi-agent AI (powered by Pydantic AI) to help software engineering students prepare for technical interviews. The platform:

1. **Analyzes your resume** to extract skills and experience level
2. **Generates tailored interview questions** based on your detected skills
3. **Evaluates your answers** with AI feedback and scores
4. **Provides actionable insights** on strengths and areas for improvement

---

## 🎯 Problem Statement

Software engineering students often struggle with:

- **Lack of personalized interview prep** – Generic questions don't match their skill levels
- **No real-time feedback** – Interview prep feels isolated and unvalidated
- **Time constraints** – Finding quality mentors or preparation resources is expensive
- **Confidence gaps** – Limited practice opportunities before real interviews

CodeClutch solves this by providing **free, instant, AI-powered interview coaching** tailored to each student's background.

---

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI (Python web framework)
- **LLM Integration**: [Pydantic AI](https://github.com/pydantic/pydantic-ai) with OpenRouter
- **Free LLM Model**: `nvidia/nemotron-3-nano-30b-a3b:free` (via OpenRouter)
- **Data Validation**: Pydantic v2
- **Environment Management**: Python dotenv
- **Deployment**: Render (Docker-ready)

### Frontend

- **Framework**: React 19 with Vite
- **Styling**: Modern CSS with responsive design
- **API Client**: Native Fetch API
- **Deployment**: Vercel
- **Environment**: Vite with env variables for production API URL

### Infrastructure

- **Backend Deployment**: Render (https://codeclutch-backend.onrender.com)
- **Frontend Deployment**: Vercel (pending deployment URL)
- **API Communication**: REST with JSON payloads

---

## 🏗️ Architecture

### Multi-Agent System (Pydantic AI)

CodeClutch uses **three specialized AI agents**, each with a defined role and Pydantic output schema:

#### 1. **ResumeAnalysisAgent**

- **Input**: Raw resume text
- **Process**: Analyzes and extracts structured data
- **Output**: Name, skills, projects, experience level
- **Schema**: `ResumeAnalysis` (Pydantic model with validation)

#### 2. **QuestionGenerationAgent**

- **Input**: List of candidate skills
- **Process**: Creates tailored interview questions
- **Output**: 5 questions with varying difficulty levels (basic, medium, hard, deep_dive)
- **Schema**: `QuestionSet` with `InterviewQuestion` items

#### 3. **AnswerEvaluationAgent**

- **Input**: Question-answer pairs
- **Process**: Evaluates each answer with scoring and feedback
- **Output**: Scores (0-10), feedback, strengths, improvements, overall readiness
- **Schema**: `InterviewFeedback` with `AnswerEvaluation` items

### Why Pydantic AI?

1. **Type Safety**: Ensures all agent outputs conform to strict Pydantic schemas
2. **Error Handling**: Built-in validation with retry logic
3. **Structured Output**: LLM responses are guaranteed to be valid JSON matching our models
4. **Production-Ready**: Easy integration with FastAPI endpoints
5. **Reliability**: Automatic retries on failures (1 retry per agent call)
6. **Cost-Effective**: Works with free OpenRouter LLM models

---

## 📋 Data Flow

```
User Uploads Resume
        ↓
[FastAPI Endpoint] → /analyze-resume
        ↓
[ResumeAnalysisAgent] (Pydantic AI)
        ↓
Return: ResumeAnalysis (name, skills, projects, experience_level)
        ↓
Generate Interview Questions
        ↓
[FastAPI Endpoint] → /generate-questions
        ↓
[QuestionGenerationAgent] (Pydantic AI)
        ↓
Return: QuestionSet (5 questions with difficulty/skill_focus)
        ↓
User Answers Questions
        ↓
[FastAPI Endpoint] → /evaluate-answers
        ↓
[AnswerEvaluationAgent] (Pydantic AI)
        ↓
Return: InterviewFeedback (scores, feedback, strengths, improvements)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Free OpenRouter API key: https://openrouter.ai/keys

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/codeclutch.git
   cd codeclutch
   ```

2. **Create Python environment**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenRouter API key:

   ```
   OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
   ```

5. **Run development server**
   ```bash
   uvicorn main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Create environment file (optional for local dev)**

   ```bash
   cp .env.example .env.local
   # For local testing, set: VITE_API_BASE=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

---

## 📦 API Endpoints

### Health Check

```
GET /
Response: { "message": "CodeClutch API is running", "status": "active" }
```

### Analyze Resume (Text)

```
POST /analyze-resume
Request: { "resume_text": "string" }
Response: {
  "name": "string",
  "skills": ["string"],
  "projects": ["string"],
  "experience_level": "beginner|intermediate|advanced"
}
```

### Analyze Resume (PDF)

```
POST /analyze-resume-pdf
Request: multipart/form-data (file upload)
Response: Same as /analyze-resume
```

### Generate Interview Questions

```
POST /generate-questions
Request: { "skills": ["string"] }
Response: {
  "questions": [
    {
      "question": "string",
      "difficulty": "basic|medium|hard|deep_dive",
      "skill_focus": "string"
    }
  ]
}
```

### Evaluate Answers

```
POST /evaluate-answers
Request: {
  "qa_pairs": [
    { "question": "string", "answer": "string" }
  ]
}
Response: {
  "evaluations": [
    {
      "question": "string",
      "score": 0-10,
      "feedback": "string"
    }
  ],
  "strengths": ["string"],
  "improvements": ["string"],
  "overall_readiness_summary": "string"
}
```

---

## 🌐 Deployment

### Backend (Render)

1. **Create Render account** at https://render.com
2. **Connect GitHub repository**
3. **Create new Web Service**
   - Environment: Python 3.11
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variable**
   - Name: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key
5. **Deploy** – Render will automatically build and deploy

### Frontend (Vercel)

1. **Create Vercel account** at https://vercel.com
2. **Connect GitHub repository**
3. **Create new project** (auto-detect Vite)
4. **Set environment variable**
   - Name: `VITE_API_BASE`
   - Value: Your Render backend URL (e.g., `https://codeclutch-backend.onrender.com`)
5. **Deploy** – Vercel will build and deploy automatically

#### Production Deployment Links

- **Backend**: https://codeclutch-backend.onrender.com
- **Frontend**: https://codeclutch.vercel.app (pending)

---

## 🔒 Security & Best Practices

1. **Environment Variables**: All sensitive data (API keys) loaded from `.env` files
2. **CORS Configuration**: FastAPI CORS middleware configured for production
3. **Input Validation**: All inputs validated with Pydantic schemas
4. **Error Handling**: Comprehensive error handling with try/except and HTTPException
5. **Retry Logic**: LLM calls retry once on failure
6. **No Hardcoded Secrets**: API keys never committed to version control

---

## 🧪 Testing

### Test the API locally

```bash
# Terminal 1: Run backend
cd backend
uvicorn main:app --reload

# Terminal 2: Test with curl
curl -X POST http://localhost:8000/analyze-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python, JavaScript, React, FastAPI, 3 years experience"}'
```

### Test the frontend

```bash
# Terminal 1: Run backend
cd backend && uvicorn main:app --reload

# Terminal 2: Run frontend
cd frontend && npm run dev
# Visit http://localhost:5173
```

---

## 📊 One-Minute Demo Walkthrough

1. **Upload Resume**: Paste your resume text into the textarea
2. **Extract Skills**: Click "Extract Skills" → AI analyzes your background (1-2 seconds)
3. **Generate Questions**: Click "Generate Interview Questions" → Receive 5 tailored questions (2-3 seconds)
4. **Answer Questions**: Type thoughtful answers for each question
5. **Get Feedback**: Click "Get AI Feedback" → Receive scores (0-10), detailed feedback, strengths, and improvement areas (3-5 seconds)
6. **Review Results**: See your interview readiness assessment
7. **Start Over**: Click "Start New Interview Session" for another practice round

**Total time**: ~2-3 minutes per interview session

---

## 🤔 Why Pydantic AI for This Project?

### Problem Without Pydantic AI

- Manual JSON parsing and validation of LLM responses
- Fragile string matching for output parsing
- No type safety – output structure unknown until runtime
- Difficult to handle partial/malformed responses
- Higher failure rates in production

### Solution with Pydantic AI

✅ **Declarative Schemas**: Define exactly what we expect from each agent  
✅ **Automatic Validation**: Pydantic validates every LLM response  
✅ **Type Safety**: Full Python type hints on all outputs  
✅ **Error Recovery**: Built-in retry logic on validation failures  
✅ **FastAPI Integration**: Seamless integration with existing endpoints  
✅ **Free & Production-Ready**: Works with free LLM models on OpenRouter

### Example: Without Pydantic AI

```python
# Manual parsing – fragile and error-prone
response = llm.call(prompt)
try:
    data = json.loads(response)
    name = data.get("name", "Unknown")
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        skills = [skills]  # Handle edge cases
    # ... more manual validation
except json.JSONDecodeError:
    # Retry? Log? Give up?
    raise Exception("Failed to parse LLM response")
```

### Example: With Pydantic AI

```python
# Type-safe, validated, automatic
result = agent.run_sync(
    user_prompt=...,
    result_type=ResumeAnalysis,  # Strict schema
)
analysis = result.data  # Already validated!
# analysis.name, analysis.skills, analysis.projects guaranteed valid
```

---

## 📚 Project Structure

```
codeclutch/
├── backend/
│   ├── main.py                 # FastAPI app & endpoints
│   ├── agents/
│   │   ├── resume_agent.py     # Pydantic AI: ResumeAnalysisAgent
│   │   ├── question_agent.py   # Pydantic AI: QuestionGenerationAgent
│   │   └── evaluation_agent.py # Pydantic AI: AnswerEvaluationAgent
│   ├── schemas/
│   │   ├── resume.py           # ResumeAnalysis Pydantic model
│   │   ├── questions.py        # QuestionSet Pydantic model
│   │   └── evaluation.py       # InterviewFeedback Pydantic model
│   ├── utils/
│   │   └── pdf_parser.py       # PDF extraction utility
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── runtime.txt             # Python version for Render
│   └── Procfile                # Render deployment config
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Responsive styling
│   │   ├── main.jsx            # React entry point
│   │   └── assets/
│   │       └── logo.png        # CodeClutch logo
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── .env.example            # Environment template
│   └── eslint.config.js        # Linting config
├── Procfile                    # Backend deployment for Render
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🐛 Troubleshooting

### Backend won't start

```
Error: OPENROUTER_API_KEY is not set
Solution: Create .env file with your API key from https://openrouter.ai/keys
```

### LLM calls timing out

```
Error: Request timeout after 60 seconds
Solution: Check internet connection, verify OpenRouter API is responsive
```

### Frontend can't reach backend

```
Error: Failed to fetch API response
Solution: Verify VITE_API_BASE environment variable points to running backend
For local dev: VITE_API_BASE=http://localhost:8000
```

### CORS errors

```
Error: CORS policy: No 'Access-Control-Allow-Origin' header
Solution: Backend CORS middleware is already configured, verify in production
```

---

## 📈 Future Enhancements

- [ ] User authentication and progress tracking
- [ ] Resume upload with automatic text extraction
- [ ] Interview recording and analysis
- [ ] Mock interview with timed questions
- [ ] Performance analytics dashboard
- [ ] Community benchmarking
- [ ] More LLM models (GPT-4, Claude, etc.)
- [ ] Multi-language support
- [ ] Mobile app version

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Report bugs
2. Suggest features
3. Submit pull requests

---

## 📞 Support

For issues, questions, or feedback:

- Create an issue in the GitHub repository
- Check existing issues for solutions
- Review deployment logs on Render/Vercel

---

## 🙏 Acknowledgments

- **Pydantic AI** for robust LLM agent framework
- **OpenRouter** for free LLM API access
- **FastAPI** for modern Python web framework
- **React + Vite** for fast frontend development
- **Render & Vercel** for seamless deployment

---

**Made with ❤️ for software engineering students**

_Last Updated: January 2026_
=======
# CodeClutch

AI-powered interview preparation platform for software engineering candidates. The backend analyzes resumes, generates targeted interview questions, and scores answers with actionable feedback. The frontend provides a guided, single-page experience to run the full flow.

## Features

- Resume analysis from pasted text or PDF to extract skills, projects, and experience level
- Skill-aware question generation with balanced difficulty (basic, medium, hard, deep-dive)
- Answer evaluation with 0-10 scoring, strengths, improvement tips, and readiness summary
- FastAPI backend with automatic docs (Swagger/ReDoc) and CORS enabled for the React client
- Vite + React frontend for an end-to-end interview practice session

## Architecture

- **Backend**: FastAPI, Pydantic, OpenRouter LLM calls, PDF parsing via PyPDF2. See [backend/README.md](backend/README.md) for API details.
- **Frontend**: React (Vite). Calls backend endpoints to run the analyze → generate → evaluate flow. UI lives in [frontend/src](frontend/src).

## Project Structure

```
codeclutch-backend-clean/
├─ README.md                # Root guide (this file)
├─ backend/                 # FastAPI service
│  ├─ main.py               # API entrypoint
│  ├─ requirements.txt      # Backend dependencies
│  ├─ agents/               # LLM-powered agents
│  │  ├─ resume_agent.py
│  │  ├─ question_agent.py
│  │  └─ evaluation_agent.py
│  ├─ schemas/              # Pydantic models
│  │  ├─ resume.py
│  │  ├─ questions.py
│  │  └─ evaluation.py
│  └─ utils/                # Helpers (PDF parsing, cleaning)
│     └─ pdf_parser.py
└─ frontend/                # React SPA (Vite)
  ├─ package.json          # Frontend dependencies/scripts
  ├─ vite.config.js        # Vite config
  └─ src/                  # App source
    ├─ App.jsx            # Main UI flow
    ├─ App.css            # Styling
    ├─ main.jsx           # React entry
    └─ assets/            # Static assets (logo, etc.)
```

## Prerequisites

- Python 3.10+
- Node.js 20+ and npm
- OpenRouter API key (set `OPENROUTER_API_KEY` in your environment)

## Quickstart

### Backend (FastAPI)

1. Install dependencies

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate  # on Windows
pip install -r requirements.txt
```

2. Configure environment

```bash
# in backend/.env
OPENROUTER_API_KEY=your_api_key_here
```

3. Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: http://localhost:8000/docs

### Frontend (React + Vite)

1. Install dependencies

```bash
cd frontend
npm install
```

2. Point the UI at your backend (optional)

- The default base URL in `frontend/src/App.jsx` is `https://codeclutch-backend.onrender.com`.
- For local development, change `API_BASE` to `http://localhost:8000` before running.

3. Run the dev server

```bash
npm run dev
```

Open the shown localhost port (typically http://localhost:5173).

## Usage (API examples)

Analyze resume text:

```bash
curl -X POST http://localhost:8000/analyze-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Jane Doe\\nSkills: Python, React, AWS"}'
```

Generate questions from extracted skills:

```bash
curl -X POST http://localhost:8000/generate-questions \
  -H "Content-Type: application/json" \
  -d '{"skills":["Python","React","AWS"]}'
```

Evaluate answers:

```bash
curl -X POST http://localhost:8000/evaluate-answers \
  -H "Content-Type: application/json" \
  -d '{"qa_pairs":[{"question":"What is React's virtual DOM?","answer":"It is a lightweight in-memory tree..."}]}'
```

## Configuration

- `OPENROUTER_API_KEY` (required): OpenRouter API token used by all LLM agents.
- CORS is currently open to `*`; tighten this in production.
- PDF uploads: only `.pdf` files are accepted for `/analyze-resume-pdf`.

## Getting Help

- API docs: run the backend and visit `/docs` or `/redoc`.
- Issues: use GitHub Issues for bugs or feature requests.
- Questions: open a discussion or issue with clear reproduction steps.

## Contributing

- Check existing issues and milestones before starting work.
- Open a small PR referencing the issue; include concise tests or manual steps.
- Keep secrets out of commits; use `.env` locally. If you add docs, prefer linking them from this README rather than inlining lengthy guides.

## Maintainers

- Primary maintainer: project team at CodeClutch. Contributions are welcome via pull requests.

## License

- See LICENSE (if present in the repository).
>>>>>>> c8ec66de971162872cb2e6e144908d6ae805b90b
