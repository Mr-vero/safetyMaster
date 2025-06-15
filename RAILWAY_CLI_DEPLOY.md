# 🚀 Deploy SafetyMaster Pro via Railway CLI

## Quick Terminal Deployment (2 Minutes)

### Step 1: Install Railway CLI
```bash
# macOS (using Homebrew)
brew install railway

# Or using npm (cross-platform)
npm install -g @railway/cli

# Or using curl (Linux/macOS)
curl -fsSL https://railway.app/install.sh | sh
```

### Step 2: Login to Railway
```bash
railway login
```
This opens your browser to authenticate with GitHub.

### Step 3: Deploy Your App
```bash
# Navigate to your project directory
cd /Users/whitmanwendelken/Reza/safetyMaster

# Initialize Railway project
railway init

# Deploy immediately
railway up
```

That's it! 🎉 Your app will be live in ~2 minutes.

## 📋 Complete Terminal Workflow

### Initial Setup
```bash
# 1. Install Railway CLI
brew install railway

# 2. Login
railway login

# 3. Navigate to project
cd /Users/whitmanwendelken/Reza/safetyMaster

# 4. Initialize Railway project
railway init
# Choose: "Empty Project" → Enter project name: "safetymaster-pro"

# 5. Deploy
railway up
```

### Environment Variables (Optional)
```bash
# Set production environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-super-secret-key-here

# View all variables
railway variables
```

### Useful Commands
```bash
# Check deployment status
railway status

# View logs
railway logs

# Open app in browser
railway open

# Get app URL
railway domain

# Redeploy after changes
git add .
git commit -m "Update app"
railway up

# Connect to database (if needed later)
railway add postgresql
```

## 🔧 Advanced CLI Features

### Custom Domain
```bash
# Add custom domain
railway domain add yourdomain.com

# List domains
railway domain list
```

### Environment Management
```bash
# Create staging environment
railway environment create staging

# Switch environments
railway environment use staging
railway environment use production

# Deploy to specific environment
railway up --environment production
```

### Database Integration
```bash
# Add PostgreSQL database
railway add postgresql

# Add Redis cache
railway add redis

# View database connection info
railway variables
```

## 📊 Monitoring & Management

### Real-time Logs
```bash
# Follow logs in real-time
railway logs --follow

# Filter logs by service
railway logs --service web

# View last 100 lines
railway logs --tail 100
```

### Project Management
```bash
# List all projects
railway list

# Switch projects
railway use project-name

# Delete project (careful!)
railway delete
```

## 🚀 One-Command Deploy Script

Create a deployment script for easy updates:

```bash
# Create deploy.sh
cat > deploy.sh << 'EOF'
#!/bin/bash
echo "🚀 Deploying SafetyMaster Pro to Railway..."

# Commit changes
git add .
git commit -m "Deploy: $(date)"

# Deploy to Railway
railway up

# Open app
echo "✅ Deployment complete!"
railway open
EOF

# Make executable
chmod +x deploy.sh

# Use it
./deploy.sh
```

## 🎯 Expected Output

When you run `railway up`, you'll see:
```
🚀 Building...
📦 Packaging...
🔄 Deploying...
✅ Deployment successful!

🌐 Your app is live at: https://safetymaster-pro-production.railway.app
```

## 🔍 Troubleshooting

### CLI Installation Issues
```bash
# Check if Railway CLI is installed
railway --version

# Update CLI
brew upgrade railway  # macOS
npm update -g @railway/cli  # npm
```

### Authentication Issues
```bash
# Re-login if needed
railway logout
railway login
```

### Deployment Issues
```bash
# Check project status
railway status

# View detailed logs
railway logs --follow

# Restart deployment
railway up --force
```

## 💡 Pro Tips

1. **Use `railway logs --follow`** during deployment to see real-time progress
2. **Set up environment variables** before first deployment
3. **Use `railway open`** to quickly access your deployed app
4. **Create aliases** for common commands:
   ```bash
   alias rdeploy="railway up"
   alias rlogs="railway logs --follow"
   alias ropen="railway open"
   ```

## 🎉 Ready to Deploy?

Run these commands now:
```bash
# Install CLI
brew install railway

# Login
railway login

# Deploy
cd /Users/whitmanwendelken/Reza/safetyMaster
railway init
railway up
```

Your SafetyMaster Pro will be live in 2 minutes! 🛡️✨ 