#!/bin/bash

# SafetyMaster Pro - Railway Deployment Script
echo "🛡️ SafetyMaster Pro - Railway Deployment"
echo "========================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    if command -v brew &> /dev/null; then
        brew install railway
    elif command -v npm &> /dev/null; then
        npm install -g @railway/cli
    else
        echo "Please install Railway CLI manually:"
        echo "curl -fsSL https://railway.app/install.sh | sh"
        exit 1
    fi
fi

echo "✅ Railway CLI found"

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

echo "✅ Authenticated with Railway"

# Commit any changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy SafetyMaster Pro: $(date)" || echo "No changes to commit"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment Successful!"
    echo "========================"
    echo ""
    echo "Your SafetyMaster Pro is now live!"
    echo ""
    echo "Commands to manage your deployment:"
    echo "  railway open     - Open app in browser"
    echo "  railway logs     - View application logs"
    echo "  railway status   - Check deployment status"
    echo "  railway domain   - Get app URL"
    echo ""
    
    # Ask if user wants to open the app
    read -p "🌐 Open app in browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        railway open
    fi
else
    echo "❌ Deployment failed. Check logs with: railway logs"
    exit 1
fi 