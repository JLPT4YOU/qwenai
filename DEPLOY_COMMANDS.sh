#!/bin/bash
# 🚀 Quick Deployment Commands

echo "========================================"
echo "  Qwen API - Deployment Commands"
echo "========================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "\n${BLUE}Step 1: Initialize Git${NC}"
echo "git init"
echo "git add ."
echo 'git commit -m "Initial commit: Qwen Personal API"'

echo -e "\n${BLUE}Step 2: Push to GitHub${NC}"
echo "# Create repo on GitHub first, then:"
echo "git remote add origin https://github.com/YOUR_USERNAME/qwen-api.git"
echo "git push -u origin main"

echo -e "\n${BLUE}Step 3: Deploy to Vercel${NC}"
echo "# Option A: Web Interface"
echo "# 1. Go to https://vercel.com/new"
echo "# 2. Import your GitHub repo"
echo "# 3. Add environment variables:"
echo "#    QWEN_TOKEN=your_token"
echo "#    ADMIN_KEY=random_secure_string"
echo "# 4. Deploy"
echo ""
echo "# Option B: CLI"
echo "npm i -g vercel"
echo "vercel"
echo "vercel env add QWEN_TOKEN production"
echo "vercel env add ADMIN_KEY production"
echo "vercel --prod"

echo -e "\n${BLUE}Step 4: Test Your API${NC}"
echo 'curl https://your-project.vercel.app/health'
echo ""
echo 'curl -X POST https://your-project.vercel.app/api/chat/quick \'
echo '  -H "Authorization: Bearer YOUR_TOKEN" \'
echo '  -d '"'"'{"message": "Hello!"}'"'"

echo -e "\n${GREEN}✅ Ready to deploy!${NC}"
echo ""
echo "Quick links:"
echo "  📖 README.md - Project overview"
echo "  ⚡ QUICKSTART.md - 5-minute setup"
echo "  📚 API_DOCS.md - API reference"
echo "  🚀 DEPLOY.md - Detailed deployment guide"
echo ""
echo "Need help? Check the docs folder!"
