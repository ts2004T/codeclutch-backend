# CodeClutch Quick Start Guide

## 🚀 Start Developing Locally (2 minutes)

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with your OpenRouter API key
# Get free key: https://openrouter.ai/keys
echo OPENROUTER_API_KEY=sk-or-v1-your-key-here > .env

# 5. Run backend
uvicorn main:app --reload
# ✅ Backend running at http://localhost:8000
# 📖 API docs at http://localhost:8000/docs
```

### Frontend Setup (in new terminal)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run frontend
npm run dev
# ✅ Frontend running at http://localhost:5173
```

**That's it! Open http://localhost:5173 and start preparing!**

---

## 🌐 Deploy to Production (5 minutes each)

### Deploy Backend to Render

1. **Push code to GitHub**

   ```bash
   git add .
   git commit -m "CodeClutch ready for production"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to https://render.com/dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Name**: codeclutch-backend
     - **Environment**: Python 3
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free

3. **Add Environment Variable**
   - In Render dashboard, go to Environment
   - Add: `OPENROUTER_API_KEY` = `sk-or-v1-your-key-here`
   - Deploy

4. **Copy your backend URL** (e.g., https://codeclutch-backend.onrender.com)

### Deploy Frontend to Vercel

1. **Push code to GitHub** (if not done already)

2. **Create Vercel Project**
   - Go to https://vercel.com/dashboard
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Click "Continue"

3. **Configure Build Settings**
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist` (auto-detected)

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add: `VITE_API_BASE` = `https://codeclutch-backend.onrender.com`
   - Click "Deploy"

5. **Done!** Your site is live at `https://your-project-name.vercel.app`

---

## ✅ Verify Your Deployment

### Test Backend API

```bash
curl -X POST https://your-backend.onrender.com/analyze-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python developer with 3 years experience"}'
```

### Test Frontend

- Visit your Vercel URL
- Upload a resume
- Generate questions
- Submit answers
- See feedback

---

## 🆘 Troubleshooting

| Problem                         | Solution                                                     |
| ------------------------------- | ------------------------------------------------------------ |
| `OPENROUTER_API_KEY is not set` | Get free key from https://openrouter.ai/keys and add to .env |
| Backend won't start             | Run `pip install -r requirements.txt`                        |
| Frontend can't connect          | Check `VITE_API_BASE` in .env file                           |
| Render build fails              | Push `Procfile` and `runtime.txt` files to GitHub            |
| Vercel build fails              | Ensure `package.json` is in `frontend/` directory            |

---

## 📚 Full Documentation

- **Project Overview**: See [README.md](README.md)
- **Backend Details**: See [backend/README.md](backend/README.md)
- **Refactor Summary**: See [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)

---

## 🎯 What's Inside

- ✅ **Pydantic AI Agents**: Type-safe LLM integration
- ✅ **FastAPI Backend**: Production-ready REST API
- ✅ **React Frontend**: Modern, responsive UI
- ✅ **Error Handling**: Robust with automatic retries
- ✅ **Deployment Ready**: Render + Vercel configuration
- ✅ **Free LLM**: Using OpenRouter free tier (nvidia/nemotron-3-nano-30b-a3b:free)

---

## 🚀 You're All Set!

Your CodeClutch interview prep platform is ready to help students prepare for technical interviews.

**Questions?** Check [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) or [README.md](README.md)

Happy interviewing! 🎓
