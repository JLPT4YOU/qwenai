# 🚀 Deploy to Vercel - Complete Guide

## ✅ Giải Pháp: Token Expires? KHÔNG CẦN Update Code!

### 3 Cách Xử Lý Token Expiry

---

## 🎯 Solution 1: Environment Variables (Recommended)

### Setup Ban Đầu

1. **Push code lên GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy lên Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

3. **Set Environment Variables**
```bash
# Via CLI
vercel env add QWEN_TOKEN production
# Paste your token when prompted

vercel env add ADMIN_KEY production
# Enter a secure random key
```

**Or via Dashboard:**
- Go to Vercel Dashboard
- Your Project → Settings → Environment Variables
- Add:
  - `QWEN_TOKEN` = your-token
  - `ADMIN_KEY` = your-secure-key

### Khi Token Expires (Sau 7 ngày)

**Option A: Via Dashboard (Easy)**
```
1. Vercel Dashboard → Settings → Environment Variables
2. Edit QWEN_TOKEN → Paste new token
3. Redeploy (1 click) - DONE!
```

**Option B: Via CLI**
```bash
vercel env rm QWEN_TOKEN production
vercel env add QWEN_TOKEN production
# Paste new token

vercel --prod  # Redeploy
```

**⏱️ Time:** 30 seconds  
**Code changes:** NONE! ✅

---

## 🏆 Solution 2: Admin API (Best for Automation!)

### Setup

Deploy với admin endpoint (đã có trong `api_server.py`):

```python
# Already implemented!
@app.route('/api/admin/token', methods=['POST'])
def update_token():
    """Update token without redeploying"""
    # Protected by admin_key
```

### Khi Token Expires

**Update token via API call - NO REDEPLOY NEEDED!**

```bash
curl -X POST https://your-app.vercel.app/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "new-token-here",
    "admin_key": "your-admin-key"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Token updated successfully"
}
```

**⏱️ Time:** 5 seconds  
**Redeploy:** NOT needed! ✅  
**Code changes:** NONE! ✅

### Admin UI (Optional)

Create simple HTML admin panel:

```html
<!-- admin.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Token Admin</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        input, button { padding: 10px; margin: 5px 0; width: 100%; }
        button { background: #0070f3; color: white; border: none; cursor: pointer; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>🔑 Token Update</h1>
    
    <input type="password" id="adminKey" placeholder="Admin Key">
    <input type="text" id="newToken" placeholder="New Token">
    <button onclick="updateToken()">Update Token</button>
    
    <div id="result"></div>
    
    <script>
        const API_URL = 'https://your-app.vercel.app';
        
        async function updateToken() {
            const adminKey = document.getElementById('adminKey').value;
            const token = document.getElementById('newToken').value;
            const result = document.getElementById('result');
            
            try {
                const response = await fetch(`${API_URL}/api/admin/token`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ admin_key: adminKey, token })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    result.innerHTML = '<p class="success">✅ Token updated!</p>';
                } else {
                    result.innerHTML = `<p class="error">❌ ${data.error}</p>`;
                }
            } catch (err) {
                result.innerHTML = `<p class="error">❌ ${err.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

---

## 🤖 Solution 3: Auto Token Refresh (Advanced)

### Implement Auto-refresh

Add to `api_server.py`:

```python
import jwt
from datetime import datetime

def is_token_expiring_soon(token, days=2):
    """Check if token expires in less than N days"""
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        exp = decoded.get('exp')
        if exp:
            exp_date = datetime.fromtimestamp(exp)
            remaining = (exp_date - datetime.now()).days
            return remaining < days
    except:
        pass
    return False

# In your endpoints, check token
@app.before_request
def check_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token and is_token_expiring_soon(token):
        # Log warning or send notification
        print(f"⚠️ Token expires soon!")
```

### Setup Notification

**Email alert when token expires soon:**

```python
import smtplib
from email.mime.text import MIMEText

def send_expiry_alert(token):
    """Send email when token is expiring"""
    msg = MIMEText("Your Qwen token expires soon. Please update!")
    msg['Subject'] = '⚠️ Token Expiring'
    msg['To'] = 'your-email@example.com'
    
    # Send via SMTP
    # ... (configure your email service)
```

---

## 📁 Vercel Configuration

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
  ],
  "env": {
    "PYTHON_VERSION": "3.11"
  }
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

## 🔒 Security Best Practices

### 1. Secure Admin Key

```bash
# Generate strong key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Output: 8kJ_NxP2mQ1R7sT9vW4yZ6bC3dF5gH8j

# Set as env var
vercel env add ADMIN_KEY production
# Paste the generated key
```

### 2. IP Whitelist (Optional)

```python
ALLOWED_IPS = os.getenv('ADMIN_IPS', '').split(',')

@app.route('/api/admin/token', methods=['POST'])
def update_token():
    client_ip = request.remote_addr
    if ALLOWED_IPS and client_ip not in ALLOWED_IPS:
        return jsonify({"error": "Unauthorized IP"}), 403
    # ... rest of code
```

### 3. Rate Limiting

```bash
pip install flask-limiter
```

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/admin/token', methods=['POST'])
@limiter.limit("5 per hour")  # Max 5 updates per hour
def update_token():
    # ... code
```

---

## 🎯 Comparison

| Method | Redeploy? | Code Change? | Time | Ease |
|--------|-----------|--------------|------|------|
| **Env Vars** | ✅ Yes | ❌ No | 30s | Easy |
| **Admin API** | ❌ No | ❌ No | 5s | Best |
| **Auto Refresh** | ❌ No | ✅ One-time | Auto | Hard |

**Recommended:** Use **Admin API** (Solution 2) 🏆

---

## 📝 Step-by-Step: Complete Setup

### 1. Prepare Code

```bash
# Add .gitignore
echo ".token_storage.json
.env
__pycache__/
*.pyc
venv/" > .gitignore

# Commit
git add .
git commit -m "Add token management"
```

### 2. Deploy to Vercel

```bash
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name? qwen-api
# - Directory? ./
# - Override settings? No
```

### 3. Set Environment Variables

```bash
# Get your token
# chat.qwen.ai → F12 → Cookies → token

# Set env vars
vercel env add QWEN_TOKEN production
# Paste token

vercel env add ADMIN_KEY production
# Paste a secure key (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")

# Redeploy with env vars
vercel --prod
```

### 4. Test

```bash
# Test API
curl https://your-app.vercel.app/health

# Test token update (when needed)
curl -X POST https://your-app.vercel.app/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "new-token",
    "admin_key": "your-admin-key"
  }'
```

### 5. When Token Expires (7 days later)

**Option A: Admin API (Recommended)**
```bash
curl -X POST https://your-app.vercel.app/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "new-token-from-browser",
    "admin_key": "your-admin-key"
  }'
# Done! No redeploy needed.
```

**Option B: Vercel Dashboard**
```
1. dashboard.vercel.com → Your Project
2. Settings → Environment Variables
3. Edit QWEN_TOKEN
4. Redeploy
```

---

## 🎉 Benefits

✅ **No code updates needed**  
✅ **Update token in 5 seconds**  
✅ **No redeployment** (with Admin API)  
✅ **Secure** (admin key protected)  
✅ **Simple** (one API call)  
✅ **Automated** (can script it)

---

## 📱 Bonus: Mobile App for Token Update

```python
# Simple token update app
from flask import Flask, render_template, request

@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if request.method == 'POST':
        # Update token
        new_token = request.form.get('token')
        admin_key = request.form.get('admin_key')
        
        # Call update API
        response = requests.post(
            'https://your-app.vercel.app/api/admin/token',
            json={'token': new_token, 'admin_key': admin_key}
        )
        
        return render_template('admin.html', result=response.json())
    
    return render_template('admin.html')
```

---

## 🚀 Quick Reference

### Token Expires? Update in 3 Steps:

1. **Get new token**: `chat.qwen.ai → F12 → Cookies → token`
2. **Update via API**:
   ```bash
   curl -X POST https://your-app.vercel.app/api/admin/token \
     -H "Content-Type: application/json" \
     -d '{"token": "NEW_TOKEN", "admin_key": "YOUR_KEY"}'
   ```
3. **Done!** ✅ No redeploy needed.

---

## 🔗 Resources

- Vercel Env Vars: https://vercel.com/docs/environment-variables
- Python on Vercel: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- Flask Deployment: https://vercel.com/guides/deploying-flask-with-vercel

---

**Summary:**  
❌ **OLD:** Token expires → Update code → Commit → Push → Redeploy  
✅ **NEW:** Token expires → 1 API call → Done! (5 seconds)

**No more code updates for token changes!** 🎊
