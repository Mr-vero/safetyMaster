# Deploy SafetyMaster Pro to Render

## Why Render?
- Native Docker support
- Free tier available
- Built-in SSL certificates
- Easy scaling options
- Great for production apps

## Deploy Steps

### 1. Create render.yaml
```yaml
# render.yaml
services:
  - type: web
    name: safetymaster-pro
    env: docker
    dockerfilePath: ./Dockerfile
    port: 8080
    healthCheckPath: /
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PYTHONUNBUFFERED
        value: "1"
```

### 2. Deploy to Render
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Select "Web Service"
4. Choose your repository
5. Render auto-detects Dockerfile
6. Deploy!

### 3. Custom Domain (Optional)
- Free: `your-app.onrender.com`
- Custom: Add your domain in dashboard

## Pricing
- Free: 750 hours/month (enough for testing)
- Starter: $7/month (production ready)
- Pro: $25/month (enhanced performance)

## Camera Access Note
⚠️ **Important**: Cloud deployments can't access local cameras. 
Users need to access the app from devices with cameras (phones, laptops). 