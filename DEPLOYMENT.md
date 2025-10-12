# Deployment Guide for LLM Poem Generator

## 🚀 Recommended Deployment Options

### 1. Streamlit Cloud (Recommended)
**Best for Streamlit applications**

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `streamlit_app.py` as the main file
5. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase anon key

### 2. Heroku
**Good for full-stack applications**

1. Create a `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create a `runtime.txt`:
   ```
   python-3.12.3
   ```

3. Deploy using Heroku CLI or GitHub integration

### 3. Railway
**Modern alternative to Heroku**

1. Connect your GitHub repository
2. Railway will auto-detect Python
3. Add environment variables in Railway dashboard
4. Deploy automatically

### 4. Docker + Any Cloud Provider
**Most flexible option**

Create a `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## ❌ Why Vercel Doesn't Work Well

Vercel is designed for:
- Static sites
- Serverless functions
- JAMstack applications

Streamlit requires:
- Persistent server process
- WebSocket connections
- Long-running sessions
- File system access

## 🔧 Quick Fix for Vercel

If you must use Vercel, the current setup will show an informational page explaining the limitations and suggesting better alternatives.

## 📋 Environment Variables Required

- `OPENAI_API_KEY`: Your OpenAI API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key

## 🎯 Recommended Next Steps

1. **Use Streamlit Cloud** for the easiest deployment
2. **Keep Vercel** for any static documentation or landing pages
3. **Consider Railway or Heroku** for more control over the deployment
