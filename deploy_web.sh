#!/bin/bash

# SafetyMaster Pro - Web Deployment Guide
echo "🛡️ SafetyMaster Pro - Quick Web Deployment"
echo "=========================================="

# Commit any changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy SafetyMaster Pro: $(date)" || echo "No changes to commit"

echo ""
echo "🚀 Your SafetyMaster Pro is ready for deployment!"
echo ""
echo "Due to large AI model files, web deployment is recommended:"
echo ""
echo "📋 DEPLOYMENT STEPS:"
echo "1. Go to: https://railway.app"
echo "2. Click 'New Project'"
echo "3. Select 'Deploy from GitHub repo'"
echo "4. Choose your 'safetyMaster' repository"
echo "5. Railway will auto-detect Dockerfile and deploy!"
echo ""
echo "⏱️  Expected deployment time: 3-5 minutes"
echo "💾 Models will be downloaded automatically during build"
echo ""
echo "🌐 After deployment, you'll get a URL like:"
echo "   https://safetymaster-production.railway.app"
echo ""

# Ask if user wants to open Railway
read -p "🌐 Open Railway in browser now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "https://railway.app"
fi

echo ""
echo "✅ Ready for deployment! Follow the steps above." 