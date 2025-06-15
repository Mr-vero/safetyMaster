#!/bin/bash

# SafetyMaster Pro - Clean CLI Deployment
echo "🛡️ SafetyMaster Pro - Clean CLI Deployment"
echo "=========================================="

# Check if Railway CLI is installed
if ! command -v /opt/homebrew/bin/railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    brew install railway
fi

echo "✅ Railway CLI found"

# Check if logged in
if ! /opt/homebrew/bin/railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    /opt/homebrew/bin/railway login
fi

echo "✅ Authenticated with Railway"

# Show what will be uploaded (excluding large files)
echo "📦 Files to be uploaded (excluding Mac apps, zips, models):"
echo "   Core application files only..."

# Commit any changes
echo "📝 Committing changes..."
git add .
git commit -m "Clean deployment: $(date)" || echo "No changes to commit"

# Show deployment size estimate
echo "📊 Deployment size: ~2-3MB (models excluded)"
echo "🤖 AI models will download automatically during build"

# Deploy with optimized settings
echo "🚀 Starting clean deployment..."
echo "   Excluding: Mac apps, zip files, test files, demos"
echo "   Including: Core app, templates, requirements, Dockerfile"

# Use detached mode to avoid timeout
/opt/homebrew/bin/railway up --detach

# Check deployment status
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment Started Successfully!"
    echo "=========================="
    echo ""
    echo "📊 Monitoring deployment progress..."
    echo "   This may take 3-5 minutes for model downloads"
    echo ""
    
    # Follow logs for a bit
    echo "📋 Live deployment logs (press Ctrl+C to stop watching):"
    /opt/homebrew/bin/railway logs --follow
    
else
    echo "❌ Deployment failed. Checking logs..."
    /opt/homebrew/bin/railway logs --tail 50
    exit 1
fi 