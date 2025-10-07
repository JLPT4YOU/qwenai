# 🔴 CORS Issue & Solution

## 🚨 The Problem

**Qwen API does NOT support CORS** (Cross-Origin Resource Sharing).

This means:
- ❌ Cannot call Qwen API directly from browser JavaScript
- ❌ Even localhost gets blocked
- ❌ No `Access-Control-Allow-Origin` header in responses

**Error you see:**
```
Access to fetch at 'https://chat.qwen.ai/api/...' from origin 'http://localhost:8000' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

---

## ✅ The Solution: Proxy Server

We created a **CORS proxy server** that:
1. Receives requests from your browser
2. Forwards them to Qwen API (server-to-server, no CORS)
3. Returns responses with CORS headers enabled

```
Browser → Proxy Server (port 5001) → Qwen API
       ✅ CORS OK              ✅ No CORS needed
```

---

## 🚀 How to Run (2 Servers Required)

### Terminal 1: Proxy Server

```bash
cd /Users/nguyenbahoanglong/QWEN
python proxy_server.py
```

**Output:**
```
============================================================
  Qwen API CORS Proxy Server
============================================================

✓ Starting proxy server...
✓ Listening on: http://localhost:5001
✓ Proxying to: https://chat.qwen.ai/api
```

✅ **Keep this running!**

### Terminal 2: Web Server

```bash
cd /Users/nguyenbahoanglong/QWEN
python3 -m http.server 8000
```

**Output:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

✅ **Keep this running too!**

### Browser

Visit: **http://localhost:8000**

Enter your token and start chatting!

---

## 🔧 Architecture

```
┌─────────────┐
│   Browser   │
│ (localhost: │
│    8000)    │
└──────┬──────┘
       │ HTTP requests
       │ (CORS enabled ✅)
       ▼
┌─────────────────┐
│  Proxy Server   │
│  (port 5001)    │
│  - Flask app    │
│  - CORS headers │
└──────┬──────────┘
       │ HTTP requests
       │ (server-to-server, no CORS ✅)
       ▼
┌──────────────────┐
│   Qwen API       │
│ chat.qwen.ai/api │
└──────────────────┘
```

---

## 🎯 Proxy Features

✅ **CORS Headers**: Adds `Access-Control-Allow-Origin: *`  
✅ **Streaming Support**: Handles Server-Sent Events (SSE)  
✅ **All Methods**: GET, POST, DELETE, PUT, OPTIONS  
✅ **Token Forwarding**: Passes `Authorization` headers  
✅ **Error Handling**: Proper error responses  

---

## 📁 Files

| File | Description |
|------|-------------|
| `proxy_server.py` | Flask CORS proxy server |
| `index.html` | Web chat interface (uses proxy) |
| `CORS_SOLUTION.md` | This guide |

---

## ⚙️ Configuration

### Change Proxy Port

If port 5001 is busy:

```bash
python proxy_server.py 5002
```

Then update `index.html`:
```javascript
const API_BASE = 'http://localhost:5002/api';
```

### Proxy Code Snippet

```python
from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    auth = request.headers.get('Authorization')
    headers = {'Authorization': auth, 'Content-Type': 'application/json'}
    
    url = f"https://chat.qwen.ai/api/{path}"
    
    if request.method == 'GET':
        resp = requests.get(url, headers=headers)
    elif request.method == 'POST':
        resp = requests.post(url, headers=headers, json=request.get_json())
    
    return Response(resp.content, status=resp.status_code, 
                    headers={'Access-Control-Allow-Origin': '*'})
```

---

## 🐛 Troubleshooting

### Proxy Server Won't Start

**Error**: `Address already in use`

**Solution**: Use different port
```bash
python proxy_server.py 5002
```

### Browser Still Shows CORS Error

**Check**:
1. ✅ Is proxy server running? Check: `lsof -i :5001`
2. ✅ Is `API_BASE` in index.html set to `http://localhost:5001/api`?
3. ✅ Are you visiting `http://localhost:8000` (not `file://`)?

### Requests Timeout

**Check**:
1. ✅ Is your internet connection working?
2. ✅ Is token valid? Get new one from chat.qwen.ai
3. ✅ Check proxy logs in Terminal 1

---

## 🎯 Alternative Solutions

### 1. Use Python Client (No Proxy Needed) ⭐

```bash
python chatbot.py
```

- ✅ No CORS issues
- ✅ No proxy needed
- ✅ No browser needed
- ❌ No web UI

### 2. Browser Extension (Not Recommended)

Install CORS extension like "CORS Unblock"

- ✅ No proxy needed
- ❌ Security risk
- ❌ Not for production

### 3. Electron App (Future)

Package as Electron app (uses Node.js, no CORS)

- ✅ Native app experience
- ✅ No proxy needed
- ❌ More complex setup

---

## 📊 Comparison

| Method | CORS Issue | Setup Complexity | Best For |
|--------|------------|------------------|----------|
| **Python CLI** | ✅ No | ⭐ Easy | Quick use |
| **Web + Proxy** | ✅ Solved | ⭐⭐ Medium | Web UI |
| **Direct Browser** | ❌ Yes | N/A | Not possible |
| **CORS Extension** | ✅ Bypassed | ⭐ Easy | Dev only |

---

## 🏁 Quick Start Commands

```bash
# Terminal 1
python proxy_server.py

# Terminal 2  
python3 -m http.server 8000

# Browser
# Visit: http://localhost:8000
```

**That's it!** 🎉

---

## 📚 More Info

- `RUN_WEB_CHAT.md` - Detailed setup guide
- `HOW_TO_RUN_HTML.md` - Web server details
- `START_HERE.md` - Project overview

---

**Created**: 2025-10-07  
**Status**: ✅ Working & Tested  
**Servers Running**: 
- Proxy: port 5001 (PID: 77740)
- Web: port 8000 (PID: 74532)
