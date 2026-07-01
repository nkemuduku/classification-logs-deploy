# Deployment Guide - Render

This guide walks you through deploying the Log Classification API on Render.

## Prerequisites

1. **Render Account**: Sign up at [https://render.com](https://render.com)
2. **GitHub Repository**: Your project should be pushed to GitHub (already done: https://github.com/nkemuduku/classification-logs)
3. **API Keys**: You'll need a Groq API key for LLM classification

## Step 1: Prepare Environment Variables

1. Go to your Render Dashboard
2. Create environment variables needed for the app:
   - `GROQ_API_KEY`: Your Groq API key from https://console.groq.com
   - `HF_TOKEN` (optional): HuggingFace token for faster model downloads

## Step 2: Deploy via Render Dashboard

### Option A: Using Render Dashboard (Recommended)

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository:
   - Select: `nkemuduku/classification-logs`
   - Branch: `main`
4. Fill in the details:
   - **Name**: `classification-logs-api`
   - **Runtime**: `Python 3.13`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Select Plan: **Free** (or paid if you want better performance)
6. Add environment variables:
   - `GROQ_API_KEY` = (paste your API key)
   - `PYTHONUNBUFFERED` = `1`
7. Click **Create Web Service**

### Option B: Using render.yaml (Infrastructure as Code)

1. The `render.yaml` file is already configured in the repo
2. Connect your GitHub repo to Render
3. Render will automatically detect and use `render.yaml`

## Step 3: Monitor Deployment

1. After clicking "Create Web Service", Render will:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start the FastAPI server

2. Monitor the build logs in the Render dashboard
3. Once deployed, you'll get a public URL like: `https://classification-logs-api.onrender.com`

## Step 4: Test the Deployment

Once deployed, test your API:

```bash
# Health check
curl https://classification-logs-api.onrender.com/health

# Interactive API docs
https://classification-logs-api.onrender.com/docs

# Single classification
curl -X POST https://classification-logs-api.onrender.com/classify \
  -H "Content-Type: application/json" \
  -d '{
    "source": "LegacyCRM",
    "log_message": "Invoice generation failed due to tax calculation error"
  }'

# Batch classification
curl -X POST https://classification-logs-api.onrender.com/classify-batch \
  -H "Content-Type: application/json" \
  -d '{
    "logs": [
      {
        "source": "ModernCRM",
        "log_message": "IP 192.168.133.114 blocked due to attack"
      },
      {
        "source": "BillingSystem",
        "log_message": "User User12345 logged in"
      }
    ]
  }'
```

## Important Notes

### Model Loading
- **First Request Delay**: The first request may take 30-60 seconds as models (BERT, transformers) are loaded into memory
- This is normal and only happens on cold start

### Free Tier Limitations
- **Idle Timeout**: Service spins down after 15 minutes of inactivity
- **Memory**: Limited to 512MB RAM (may need upgrade for large models)
- **CPU**: Shared resources

### Recommended Upgrades for Production
- **Standard Tier**: 0.5GB RAM, dedicated resources ($7/month)
- **Premium Tier**: 2GB RAM or more for better performance

### Database & Storage
- If you need persistent storage, use:
  - Render Disk for temporary storage
  - PostgreSQL on Render for structured data
  - AWS S3 for file uploads

## Troubleshooting

### Build Fails: "Module not found"
- Check `requirements.txt` has all dependencies
- Ensure `pyproject.toml` and `requirements.txt` are synced

### Deployment Stuck
- Check build logs in Render dashboard
- Ensure GitHub push completed successfully
- Verify environment variables are set

### API Returns 500 Error
- Check service logs: Render Dashboard → Service → Logs
- Ensure `GROQ_API_KEY` is properly set
- Verify model downloads completed

### Service Spins Down (Free Tier)
- Free tier services sleep after 15 min of inactivity
- First request after sleep takes longer
- Upgrade to Standard tier for always-on service

## Custom Domain

To use a custom domain:

1. Go to Render Dashboard → Web Service Settings
2. Under "Custom Domain", add your domain
3. Update your DNS records (Render will provide instructions)

## Monitoring & Logs

View live logs:
```bash
# In Render dashboard under Logs tab
# Or via Render CLI
render logs --service classification-logs-api
```

## Rollback

If deployment fails:
1. Go to Render Dashboard → Web Service
2. Click "Manual Deploy" to rebuild from latest commit
3. Or revert your GitHub push and redeploy

## Next Steps

1. ✅ Push all changes to GitHub
2. ✅ Create/update `requirements.txt`
3. ✅ Add `render.yaml` configuration
4. Deploy on Render Dashboard
5. Test endpoints with provided examples
6. Monitor logs and performance

---

**For more info**: https://render.com/docs/deploy-fastapi
