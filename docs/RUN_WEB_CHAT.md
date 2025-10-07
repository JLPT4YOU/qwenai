# 🚀 Run Web Chat - Quick Guide

## ⚡ TL;DR (2 Terminals Required)

```bash
# Terminal 1: Install dependencies (first time only)
pip install -r requirements.txt

# Terminal 1: Start CORS proxy server
python proxy_server.py

# Terminal 2: Start web server
python3 -m http.server 8000

# Open browser: http://localhost:8000
# Enter your token from chat.qwen.ai
# Start chatting! 🎉
```

## 🔴 Why Two Servers?

**Problem**: Qwen API doesn't support CORS (browser security restriction)

**Solution**: Use a proxy server to forward requests

- **Proxy (port 5001)**: Forwards API requests to Qwen
- **Web Server (port 8000)**: Serves the HTML interface

---

## 📋 Step-by-Step

### Step 0: Install Dependencies (First Time Only)

```bash
cd /Users/nguyenbahoanglong/QWEN
pip install -r requirements.txt
```

This installs Flask and other required packages.

### Step 1: Start Proxy Server (Terminal 1)

Open first terminal and run:

```bash
cd /Users/nguyenbahoanglong/QWEN
python proxy_server.py
```

You should see:
```
============================================================
  Qwen API CORS Proxy Server
============================================================

✓ Starting proxy server...
✓ Listening on: http://localhost:5001
✓ Proxying to: https://chat.qwen.ai/api
```

**Keep this terminal open!** ✅

### Step 2: Start Web Server (Terminal 2)

Open **second** terminal and run:

```bash
cd /Users/nguyenbahoanglong/QWEN
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

**Keep this terminal open too!** ✅

### Step 3: Open in Browser

Open your browser and visit:

**http://localhost:8000**

✅ You should see the chat interface with a beautiful gradient background

### Step 4: Get Your Token

1. Open a new tab and go to: https://chat.qwen.ai
2. Login if needed
3. Press `F12` to open Developer Tools
4. Go to **Application** tab → **Local Storage** → `https://chat.qwen.ai`
5. Find the key `token` and **copy its value**

Example token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4...
```

### Step 4: Enter Token

1. Paste the token into the input field on your chat page
2. Click **"Lưu Token"** (Save Token)
3. The token will be saved in your browser's localStorage

✅ Token is saved! You won't need to enter it again.

### Step 5: Start Chatting!

Type a message and press Enter or click Send.

Example messages to try:
- "Xin chào!"
- "What is Python?"
- "Tell me a joke"
- "Explain quantum computing"

---

## ⚠️ Troubleshooting

### CORS Error (Red Banner)

If you see:
```
⚠️ CORS ERROR: File opened directly!
```

**Problem**: You opened `index.html` by double-clicking it.

**Solution**: Use the local server (python3 -m http.server 8000)

### Port Already in Use

If you see:
```
OSError: [Errno 48] Address already in use
```

**Solution**: Use a different port
```bash
python3 -m http.server 8001
# Then visit http://localhost:8001
```

### Token Expired

If messages fail with "401" or "Token expired":

**Solution**: Get a fresh token from chat.qwen.ai (repeat Step 3)

Or click "Clear Token" button and re-enter.

### No Chats Found

If you see:
```
⚠️ Không tìm thấy chat. Vui lòng tạo chat mới trên chat.qwen.ai
```

**Solution**: 
1. Go to https://chat.qwen.ai
2. Start a new conversation
3. Come back to your local chat and try again

---

## 🎯 Features

- ✅ Real-time streaming responses
- ✅ Auto token refresh
- ✅ Beautiful UI with avatars
- ✅ Token persistence (localStorage)
- ✅ Enter to send, Shift+Enter for new line
- ✅ Scrollable chat history
- ✅ CORS detection with helpful error messages

---

## 💡 Tips

### Keep Server Running

Leave the terminal with `python3 -m http.server` running while you use the chat.

To stop the server: Press `Ctrl+C`

### Multiple Browsers/Tabs

You can open http://localhost:8000 in multiple tabs. Each tab will use its own saved token.

### Mobile Access

If your phone is on the same WiFi:

1. Find your computer's IP (e.g., 192.168.1.100)
2. Start server with: `python3 -m http.server 8000 --bind 0.0.0.0`
3. On phone, visit: `http://192.168.1.100:8000`

### Token Security

Your token is saved in browser's localStorage. Don't share your token with others!

To clear token: Click "🔄 Clear Token" button or run in browser console:
```javascript
localStorage.removeItem('qwen_token');
location.reload();
```

---

## 🐍 Alternative: Python CLI

If you prefer command-line:

```bash
# Interactive chat
python chatbot.py

# Quick message
python qwen_client.py "What is AI?"

# List chats
python qwen_client.py --list-chats
```

No web server needed for Python! 🎉

---

## 📚 More Docs

- `HOW_TO_RUN_HTML.md` - Detailed HTML setup guide
- `JAVASCRIPT_API_GUIDE.md` - API documentation
- `TOKEN_REFRESH_GUIDE.md` - Token management
- `START_HERE.md` - Project overview

---

**Happy Chatting! 💬✨**
