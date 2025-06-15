# Deploy SafetyMaster Pro to Railway

## Why Railway?
- Docker-native platform
- Built-in domain and HTTPS
- Easy GitHub integration
- Automatic deployments
- Affordable pricing (~$5-20/month)

## Quick Deploy Steps

### 1. Prepare Your Repository
```bash
# Make sure your Docker setup is ready
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your safetyMaster repository
5. Railway will auto-detect Dockerfile and deploy!

### 3. Configure Environment Variables
In Railway dashboard:
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

### 4. Access Your App
Railway provides:
- Custom domain: `your-app-name.railway.app`
- HTTPS automatically enabled
- Persistent storage for violation captures

## Pricing
- Hobby: Free tier (limited hours)
- Pro: $5/month base + usage
- Perfect for production safety monitoring

## Deploy Command
```bash
# One-click deploy button for README
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/safetyMaster)
``` 