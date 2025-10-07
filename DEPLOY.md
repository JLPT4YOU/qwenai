# 🚀 Deployment Guide

Deploy your Qwen Personal API to Vercel in 5 minutes.

---

## Prerequisites

- GitHub account
- Vercel account (free)
- Qwen token (from chat.qwen.ai)

---

## Step 1: Get Your Token

1. Go to https://chat.qwen.ai
2. Login to your account
3. Press `F12` to open DevTools
4. Go to **Application** → **Cookies** → `chat.qwen.ai`
5. Copy the value of `token`

Save this token - you'll need it!

---

## Step 2: Prepare Repository

```bash
# Clone or create your repo
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/qwen-api.git
git push -u origin main
```

---

## Step 3: Deploy to Vercel

### Option A: Via Web (Easiest)

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Configure:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. Add Environment Variables:
   ```
   QWEN_TOKEN = your_token_here
   ADMIN_KEY = generate_random_secure_string
   ```
5. Click **Deploy**

### Option B: Via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name? qwen-api
# - Directory? ./
# - Override settings? No

# Add environment variables
vercel env add QWEN_TOKEN production
# Paste your token

vercel env add ADMIN_KEY production
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
# Paste the generated key

# Deploy to production
vercel --prod
```

**Done!** Your API is live at `https://your-project.vercel.app`

---

## Step 4: Test Your API

```bash
# Test health endpoint
curl https://your-project.vercel.app/health

# Test chat
curl -X POST https://your-project.vercel.app/api/chat/quick \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

**Expected response:**
```json
{
  "success": true,
  "chat_id": "...",
  "data": {
    "content": "Hello! How can I help you today?"
  }
}
```

---

## Configuration Files

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api_server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api_server.py"
    }
  ]
}
```

### requirements.txt

```txt
Flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
sseclient-py==1.8.0
PyJWT==2.8.0
```

---

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `QWEN_TOKEN` | ✅ Yes | Your Qwen auth token | `eyJhbGciOiJIUzI1NiI...` |
| `ADMIN_KEY` | ✅ Yes | Admin API key | `random_secure_string_32` |

**Generate secure ADMIN_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## Updating Token (When Expired)

### Method 1: Admin API (5 seconds, recommended)

```bash
curl -X POST https://your-project.vercel.app/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "NEW_TOKEN_FROM_BROWSER",
    "admin_key": "YOUR_ADMIN_KEY"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Token updated successfully"
}
```

**✅ No redeployment needed!**

### Method 2: Vercel Dashboard (30 seconds)

1. Go to Vercel Dashboard
2. Your Project → Settings → Environment Variables
3. Click **Edit** on `QWEN_TOKEN`
4. Paste new token → Save
5. Click **Redeploy**

---

## Custom Domain (Optional)

1. Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain (e.g., `api.yourdomain.com`)
3. Update DNS records as instructed
4. Done! SSL automatically configured

---

## Monitoring

### View Logs

```bash
vercel logs

# Or in Dashboard
# Project → Deployments → Click deployment → Logs
```

### Check Status

```bash
curl https://your-project.vercel.app/health
```

---

## Troubleshooting

### Issue: 404 Not Found

**Cause:** Routing not configured properly

**Solution:** Ensure `vercel.json` exists and is correct

### Issue: 500 Internal Server Error

**Cause:** Missing dependencies or environment variables

**Solution:**
1. Check `requirements.txt` is complete
2. Verify `QWEN_TOKEN` is set
3. Check logs: `vercel logs`

### Issue: CORS Error

**Cause:** Missing CORS headers

**Solution:** Flask-CORS is already configured in `api_server.py`

### Issue: Token Expired

**Cause:** Token expires after ~7 days

**Solution:** Update token via admin API (see above)

---

## Security Best Practices

1. **Keep ADMIN_KEY secret** - Never commit to git
2. **Use .env for local** - Add `.env` to `.gitignore`
3. **Rotate tokens regularly** - Update every 7 days
4. **Monitor logs** - Check for suspicious activity
5. **Use HTTPS only** - Vercel provides SSL automatically

---

## Performance Optimization

1. **Edge Functions:** Vercel automatically deploys to edge
2. **Caching:** Model list cached automatically
3. **Compression:** Gzip enabled by default
4. **CDN:** Static files served via CDN

---

## Scaling

**Vercel Free Tier:**
- ✅ Unlimited requests
- ✅ 100GB bandwidth/month
- ✅ Serverless functions
- ✅ SSL included

**Pro Plan ($20/month):**
- Higher bandwidth
- Priority support
- Analytics
- Team collaboration

---

## Backup & Recovery

### Backup Token

```bash
# Save token securely
echo "QWEN_TOKEN=your_token" > .env.backup
# Store in password manager or secure location
```

### Backup Configuration

```bash
# Export environment variables
vercel env pull .env.production
# Save this file securely
```

---

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Set up custom domain (optional)
4. ✅ Configure monitoring
5. ✅ Share API with your apps!

---

## Support

- **Deployment Issues:** https://vercel.com/docs
- **API Issues:** See [API_DOCS.md](./API_DOCS.md)
- **General Help:** GitHub Issues

---

**Deployment Time:** 5 minutes  
**Monthly Cost:** $0 (Vercel free tier)  
**Uptime:** 99.9%+  

🎉 **Happy deploying!**
