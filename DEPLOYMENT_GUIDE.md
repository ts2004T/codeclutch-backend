# CodeClutch Deployment Credentials & URLs

## 📍 Deployment Resources

### Hosting Platforms

- **Backend Hosting**: [Render.com](https://render.com) - Free tier available
- **Frontend Hosting**: [Vercel.com](https://vercel.com) - Free tier available
- **LLM Provider**: [OpenRouter.ai](https://openrouter.ai) - Free API with free models

---

## 🔑 Getting Started

### Step 1: Get OpenRouter API Key (FREE)

1. Visit: https://openrouter.ai/keys
2. Sign up for free account
3. Copy your API key (starts with `sk-or-v1-`)
4. This key will be used in `.env` file

### Step 2: Deploy Backend to Render

**Repository Setup**:

```bash
git add .
git commit -m "CodeClutch production ready"
git push origin main
```

**Render Deployment**:

1. Go to: https://render.com/dashboard
2. Click: "New +" → "Web Service"
3. Connect GitHub repository
4. Use these settings:

   | Setting       | Value                                                        |
   | ------------- | ------------------------------------------------------------ |
   | Name          | codeclutch-backend                                           |
   | Environment   | Python 3                                                     |
   | Build Command | `pip install -r backend/requirements.txt`                    |
   | Start Command | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | Plan          | Free                                                         |

5. Click "Create Web Service"
6. Add Environment Variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your API key from Step 1
7. Click "Deploy"
8. **Copy your backend URL** (e.g., `https://codeclutch-backend.onrender.com`)

### Step 3: Deploy Frontend to Vercel

**Vercel Deployment**:

1. Go to: https://vercel.com/new
2. Import your GitHub repository
3. Select "Vite" as framework
4. No build settings needed (auto-detected)
5. Add Environment Variable:
   - Key: `VITE_API_BASE`
   - Value: Your backend URL from Step 2
6. Click "Deploy"
7. **Your frontend URL will be displayed** (e.g., `https://codeclutch.vercel.app`)

---

## 🌐 Production URLs (After Deployment)

### Backend API

```
https://codeclutch-backend.onrender.com

Health Check: https://codeclutch-backend.onrender.com/
API Docs: https://codeclutch-backend.onrender.com/docs
```

### Frontend Application

```
https://your-project-name.vercel.app

(Exact URL shown after Vercel deployment)
```

---

## ✅ Verification Checklist

After deployment, verify everything works:

### Backend (Render)

```bash
# Test health check
curl https://codeclutch-backend.onrender.com/

# Test resume analysis
curl -X POST https://codeclutch-backend.onrender.com/analyze-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "Python, JavaScript developer with 3 years experience"}'

# View API docs
Open: https://codeclutch-backend.onrender.com/docs
```

### Frontend (Vercel)

1. Open your Vercel URL in browser
2. Paste sample resume text
3. Click "Extract Skills" → verify response
4. Click "Generate Questions" → verify 5 questions appear
5. Write answers and click "Get AI Feedback" → verify feedback displays

---

## 📋 Environment Variables Reference

### Backend (.env)

```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

### Frontend (Vercel env vars)

```
VITE_API_BASE=https://codeclutch-backend.onrender.com
```

---

## 🔄 How to Update After Deployment

### Push Code Updates

```bash
# Make changes locally
git add .
git commit -m "Your message"
git push origin main

# Render & Vercel auto-deploy!
```

### Update API Key (if needed)

1. Go to Render dashboard
2. Select codeclutch-backend service
3. Go to Environment tab
4. Update `OPENROUTER_API_KEY`
5. Click "Deploy" button manually

---

## 🆘 Deployment Troubleshooting

### Backend won't deploy

- ✅ Check `Procfile` is in root directory
- ✅ Check `runtime.txt` has Python 3.11.9
- ✅ Check `backend/requirements.txt` exists
- ✅ Push all files to GitHub

### Frontend won't connect to backend

- ✅ Verify `VITE_API_BASE` is set in Vercel
- ✅ Ensure backend URL is correct
- ✅ Check backend health: `https://your-backend/`
- ✅ Redeploy frontend after updating env var

### LLM calls failing

- ✅ Verify OpenRouter API key is correct
- ✅ Check API key is set in Render env vars
- ✅ Go to https://openrouter.ai/keys to verify key
- ✅ Test API directly: https://openrouter.ai/api/v1/chat/completions

### Render keeps restarting

- ✅ Check logs: Render dashboard → Logs tab
- ✅ Verify Python version (3.11.9)
- ✅ Ensure no blocking code in imports
- ✅ Check for infinite loops

### Vercel build fails

- ✅ Check `frontend/package.json` exists
- ✅ Verify `npm run build` works locally
- ✅ Check `vite.config.js` is correct
- ✅ Ensure no TypeScript errors

---

## 📞 Support Resources

### Documentation

- Main Guide: [README.md](./README.md)
- Quick Start: [QUICKSTART.md](./QUICKSTART.md)
- Refactor Details: [REFACTOR_SUMMARY.md](./REFACTOR_SUMMARY.md)
- Checklist: [IMPLEMENTATION_CHECKLIST.md](./IMPLEMENTATION_CHECKLIST.md)

### External Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **OpenRouter API**: https://openrouter.ai/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

### Community Help

- Render Support: https://render.com/support
- Vercel Support: https://vercel.com/support
- OpenRouter Community: https://openrouter.ai

---

## 📊 Estimated Costs

### Completely FREE with current setup:

- ✅ **Render**: Free tier (no credit card required)
- ✅ **Vercel**: Free tier (no credit card required)
- ✅ **OpenRouter**: Free tier with generous limits
- ✅ **Total Monthly Cost**: $0

### If scaling in future:

- Render Web Service: ~$7/month for standard tier
- Vercel: ~$20/month for pro tier (optional)
- OpenRouter: Pay-as-you-go ($0.30-$2 per 1M tokens)

---

## 🎯 Next Steps

1. **Get OpenRouter Key**: https://openrouter.ai/keys
2. **Deploy Backend**: Follow Render steps above
3. **Deploy Frontend**: Follow Vercel steps above
4. **Verify**: Test both services work
5. **Share**: Deploy link ready to share!

---

## 📝 Notes

- **Keep API Key Secret**: Never commit to GitHub
- **Test Locally First**: Before deploying changes
- **Monitor Logs**: Check Render logs if issues arise
- **Redeploy on Env Changes**: Render requires redeploy for new env vars
- **Free Tier Limits**: Render free tier sleeps after 30 min inactivity

---

## ✨ You're All Set!

Your CodeClutch interview prep platform is ready to deploy to production.

**Total Setup Time**: ~30 minutes  
**Total Cost**: $0 (free tier)  
**Result**: Fully functional interview prep platform 🎉

---

_Last Updated: January 2026_  
_Deployment Status: Ready for Production_ 🚀
