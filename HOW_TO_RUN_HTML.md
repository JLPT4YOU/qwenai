# 🚀 How to Run index.html

## ⚠️ IMPORTANT: CORS Error Fix

If you open `index.html` directly by double-clicking, you'll get this error:

```
Access to fetch at 'https://chat.qwen.ai/api/v1/auths/' from origin 'null' 
has been blocked by CORS policy
```

**Reason**: Browsers block API requests from `file://` protocol for security.

**Solution**: Run a local web server!

---

## ✅ Method 1: Python HTTP Server (Recommended)

### Step 1: Start Server

```bash
cd /Users/nguyenbahoanglong/QWEN
python3 -m http.server 8000
```

Output:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

### Step 2: Open Browser

Visit: **http://localhost:8000**

✅ CORS errors will be gone!

---

## ✅ Method 2: Node.js Server

### Install http-server (once)

```bash
npm install -g http-server
```

### Run Server

```bash
cd /Users/nguyenbahoanglong/QWEN
http-server -p 8000
```

### Open Browser

Visit: **http://localhost:8000**

---

## ✅ Method 3: PHP Server

```bash
cd /Users/nguyenbahoanglong/QWEN
php -S localhost:8000
```

Visit: **http://localhost:8000**

---

## ✅ Method 4: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

Auto opens in browser with proper server!

---

## 🎯 Quick Start (Copy-Paste)

```bash
# Navigate to project
cd /Users/nguyenbahoanglong/QWEN

# Start server (Python)
python3 -m http.server 8000

# In another terminal or browser:
# Open http://localhost:8000

# Stop server: Ctrl+C
```

---

## 🔍 Verify Server is Running

### Check Terminal Output

You should see:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

### Test in Browser

1. Open: http://localhost:8000
2. You should see the chat interface
3. Check browser console (F12) - no CORS errors!

### Common Issues

#### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution**: Use different port
```bash
python3 -m http.server 8001
# Then open http://localhost:8001
```

#### Command Not Found

```
python3: command not found
```

**Solution**: Try `python` instead
```bash
python -m http.server 8000
```

---

## 📱 Access from Other Devices

### Find Your IP Address

```bash
# Mac/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

Example output: `192.168.1.100`

### Allow External Access

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

### Access from Phone/Tablet

Open: `http://192.168.1.100:8000`

⚠️ **Note**: Device must be on same WiFi network!

---

## 🛡️ Security Note

**Local development server is NOT secure for production!**

- ✅ OK for local development
- ✅ OK for same WiFi network
- ❌ NOT for internet exposure
- ❌ NOT for sensitive data

For production, use proper web hosting (nginx, Apache, etc.)

---

## 🎨 Alternative: Use Python Client Instead

If you don't want to run a web server, use the Python client:

```bash
# Interactive chat
python chatbot.py

# Quick message
python qwen_client.py "Hello"

# List chats
python qwen_client.py --list-chats
```

No CORS issues with Python! 🐍

---

## 📝 Summary

| Method | Command | Port |
|--------|---------|------|
| Python | `python3 -m http.server 8000` | 8000 |
| Node.js | `http-server -p 8000` | 8000 |
| PHP | `php -S localhost:8000` | 8000 |
| VS Code | Live Server extension | Auto |

**Always access via `http://localhost:PORT`, never `file://`**

---

**Last Updated**: 2025-10-07  
**Status**: ✅ Tested & Working
