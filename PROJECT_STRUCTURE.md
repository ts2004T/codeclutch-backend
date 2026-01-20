# CodeClutch Project Structure

```
codeclutch-backend/
│
├── 📋 DOCUMENTATION (Read these!)
│   ├── INDEX.md ⭐ START HERE - Navigation guide
│   ├── README.md (400+ lines) - Complete project guide
│   ├── QUICKSTART.md - 5-minute local setup
│   ├── DEPLOYMENT_GUIDE.md - Production deployment
│   ├── REFACTOR_SUMMARY.md - What was improved
│   ├── IMPLEMENTATION_CHECKLIST.md - Verification checklist
│   └── COMPLETION_SUMMARY.md - Executive overview
│
├── 🔧 CONFIGURATION
│   ├── Procfile - Render deployment config
│   ├── .gitignore - Git ignore rules
│   └── .git/ - Git repository
│
├── 📁 backend/ - Python FastAPI Backend
│   │
│   ├── 📄 main.py - FastAPI application & endpoints
│   │   ├── GET / - Health check
│   │   ├── POST /analyze-resume - Text resume analysis
│   │   ├── POST /analyze-resume-pdf - PDF resume analysis
│   │   ├── POST /generate-questions - Question generation
│   │   └── POST /evaluate-answers - Answer evaluation
│   │
│   ├── 🤖 agents/ - Pydantic AI Agents
│   │   ├── resume_agent.py
│   │   │   └── ResumeAnalysisAgent (Pydantic AI)
│   │   ├── question_agent.py
│   │   │   └── QuestionGenerationAgent (Pydantic AI)
│   │   └── evaluation_agent.py
│   │       └── AnswerEvaluationAgent (Pydantic AI)
│   │
│   ├── 📊 schemas/ - Pydantic Data Models
│   │   ├── resume.py
│   │   │   ├── ExperienceLevel (Enum)
│   │   │   └── ResumeAnalysis (Model)
│   │   ├── questions.py
│   │   │   ├── Difficulty (Enum)
│   │   │   ├── InterviewQuestion (Model)
│   │   │   └── QuestionSet (Model)
│   │   └── evaluation.py
│   │       ├── QuestionAnswerPair (Model)
│   │       ├── AnswerEvaluation (Model)
│   │       └── InterviewFeedback (Model)
│   │
│   ├── 🛠️ utils/ - Utility Functions
│   │   └── pdf_parser.py
│   │       ├── extract_text_from_pdf()
│   │       └── clean_resume_text()
│   │
│   ├── 📄 README.md - Backend documentation
│   ├── .env.example - Environment template
│   ├── .env - Environment variables (secrets)
│   ├── requirements.txt - Python dependencies
│   ├── runtime.txt - Python version (3.11.9)
│   ├── __pycache__/ - Python cache
│   └── __init__.py - Package initialization
│
├── 🎨 frontend/ - React + Vite Frontend
│   │
│   ├── 📄 index.html - HTML entry point
│   │   └── Favicon: logo.png
│   │   └── Title: CodeClutch – AI Interview Prep
│   │
│   ├── 📁 src/ - Source code
│   │   ├── App.jsx - Main React component
│   │   │   ├── State management (resume, skills, questions, etc.)
│   │   │   ├── API calls (analyze, generate, evaluate)
│   │   │   ├── Loading states
│   │   │   ├── Error handling
│   │   │   └── 4-step interview flow
│   │   │
│   │   ├── App.css - Professional styling
│   │   │   ├── Color variables (primary, text, bg, etc.)
│   │   │   ├── Responsive design
│   │   │   ├── Modern layout
│   │   │   ├── Button states (hover, active, disabled)
│   │   │   ├── Loading spinner animation
│   │   │   └── Card-based design
│   │   │
│   │   ├── main.jsx - React entry point
│   │   ├── index.css - Global styles
│   │   │
│   │   └── 📁 assets/ - Static files
│   │       └── logo.png - CodeClutch logo
│   │
│   ├── 📄 package.json - Node dependencies
│   │   ├── Dependencies: react@19, react-dom@19
│   │   ├── Dev Dependencies: vite, eslint, etc.
│   │   └── Scripts: dev, build, preview, lint
│   │
│   ├── vite.config.js - Vite build config
│   │   └── Environment variable support
│   │
│   ├── eslint.config.js - ESLint rules
│   ├── .env.example - Frontend env template
│   └── public/ - Public static files
│
├── 📁 venv/ - Python virtual environment
│   ├── lib/python3.11/site-packages/ - Installed packages
│   └── Scripts/ - Python executables
│
└── 📄 OPENROUTER_API_KEY=sk-or-v1-... (⚠️ Don't commit!)

```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND (React + Vite)                                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ App.jsx                                                 │ │
│ │ ├─ Step 1: Resume Input (textarea)                      │ │
│ │ ├─ Step 2: Extract Skills Button                        │ │
│ │ ├─ Step 3: Display Skills + Generate Questions Button   │ │
│ │ ├─ Step 4: Questions + Answers Textareas               │ │
│ │ └─ Step 5: Feedback Display                            │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ JSON POST/Response
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ BACKEND (FastAPI)                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ main.py Endpoints                                       │ │
│ │ ├─ POST /analyze-resume                                 │ │
│ │ ├─ POST /generate-questions                             │ │
│ │ └─ POST /evaluate-answers                               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Pydantic AI Agents                                      │ │
│ │ ├─ ResumeAnalysisAgent                                  │ │
│ │ │  └─ Output: ResumeAnalysis (validated)               │ │
│ │ ├─ QuestionGenerationAgent                              │ │
│ │ │  └─ Output: QuestionSet (validated)                  │ │
│ │ └─ AnswerEvaluationAgent                                │ │
│ │    └─ Output: InterviewFeedback (validated)            │ │
│ └─────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ LLM Service (OpenRouter)                                │ │
│ │ ├─ Model: nvidia/nemotron-3-nano-30b-a3b:free          │ │
│ │ ├─ Free tier available                                  │ │
│ │ └─ API: https://openrouter.ai/api/v1/chat/completions │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Validated Response
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND Display                                            │
│ ├─ Skills extracted and displayed                           │
│ ├─ Questions with difficulty/skill_focus shown             │
│ ├─ User answers scored 0-10                               │
│ ├─ Detailed feedback provided                              │
│ └─ Strengths & improvements listed                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Technology Stack Breakdown

### Backend

```
FastAPI (Framework)
├─ HTTP server for REST API
├─ Automatic OpenAPI documentation
└─ CORS middleware

Pydantic AI (LLM Integration)
├─ Type-safe agent framework
├─ Automatic output validation
├─ Error handling & retries
└─ Works with any LLM provider

Pydantic v2 (Data Validation)
├─ BaseModel for schemas
├─ Field validation
├─ Automatic JSON serialization
└─ Type hints support

Python-dotenv (Env Management)
└─ Load .env files

PyPDF2 (PDF Processing)
└─ Extract text from PDF files

Uvicorn (ASGI Server)
└─ Production-grade Python web server
```

### Frontend

```
React 19 (UI Framework)
├─ Component-based architecture
├─ useState for state management
└─ Hooks for side effects

Vite (Build Tool)
├─ Fast development server
├─ Optimized production build
└─ Environment variable support

CSS (Styling)
├─ Modern, responsive design
├─ Animations & transitions
├─ Mobile-first approach
└─ Professional color palette
```

### Infrastructure

```
Render (Backend Hosting)
├─ Free tier available
├─ Auto-deploys from GitHub
└─ Environment variable support

Vercel (Frontend Hosting)
├─ Free tier available
├─ Optimized for Vite
└─ Environment variable support

OpenRouter (LLM Provider)
├─ Free tier with rate limits
├─ Multiple models available
└─ No credit card required
```

---

## 🔐 Security Files (Not in Repo)

```
.env - Contains:
├─ OPENROUTER_API_KEY (secret)
└─ Should be in .gitignore

.env.example - Template for:
├─ OPENROUTER_API_KEY=sk-or-v1-your-key-here
└─ Safe to commit
```

---

## 📊 Key Files by Purpose

### Understanding the System

```
README.md              - Project overview & architecture
backend/README.md      - Backend details
frontend/index.html    - Frontend entry point
```

### Understanding Data Models

```
backend/schemas/resume.py      - Resume analysis output
backend/schemas/questions.py   - Question generation output
backend/schemas/evaluation.py  - Evaluation output
```

### Understanding Agents

```
backend/agents/resume_agent.py      - Resume analysis agent
backend/agents/question_agent.py    - Question generation agent
backend/agents/evaluation_agent.py  - Answer evaluation agent
```

### Understanding Endpoints

```
backend/main.py - All 4 REST endpoints with error handling
```

### Understanding UI

```
frontend/src/App.jsx       - Main component logic
frontend/src/App.css       - All styling & animations
frontend/src/main.jsx      - React entry point
frontend/index.html        - HTML template
```

### Configuration & Deployment

```
backend/requirements.txt - Python dependencies
backend/runtime.txt     - Python version
backend/.env.example    - Backend env template
frontend/package.json   - Node dependencies
frontend/.env.example   - Frontend env template
vite.config.js         - Vite build config
Procfile               - Render deployment
```

---

## 🚀 Deployment Locations

### Local Development

```
Backend:  http://localhost:8000
Frontend: http://localhost:5173
API Docs: http://localhost:8000/docs
```

### Production (After Deployment)

```
Backend:  https://codeclutch-backend.onrender.com
Frontend: https://your-project.vercel.app
API Docs: https://codeclutch-backend.onrender.com/docs
```

---

## ✨ Quick File Guide

| File                               | Size             | Purpose              |
| ---------------------------------- | ---------------- | -------------------- |
| README.md                          | 400+ lines       | Main documentation   |
| backend/main.py                    | ~250 lines       | FastAPI endpoints    |
| backend/agents/resume_agent.py     | ~77 lines        | Resume AI agent      |
| backend/agents/question_agent.py   | ~60 lines        | Question AI agent    |
| backend/agents/evaluation_agent.py | ~55 lines        | Evaluation AI agent  |
| frontend/src/App.jsx               | ~250 lines       | React component      |
| frontend/src/App.css               | ~400 lines       | Professional styling |
| backend/requirements.txt           | 8 dependencies   | Python packages      |
| frontend/package.json              | 10+ dependencies | Node packages        |

---

## 📈 Lines of Code Summary

```
Backend Python:        ~600 lines
├─ Agents:            ~200 lines
├─ Endpoints:         ~250 lines
└─ Schemas:           ~150 lines

Frontend JavaScript:   ~250 lines
├─ Component:         ~250 lines
└─ Styling:           ~400 lines CSS

Documentation:       1000+ lines
├─ README.md:        400+ lines
├─ Other docs:       600+ lines
└─ Comments:         100+ lines

Total:              ~3000 lines
```

---

**Project Structure: Complete ✅**  
**Documentation: Comprehensive ✅**  
**Production Ready: YES 🚀**

_Visit [INDEX.md](INDEX.md) for navigation guide_
