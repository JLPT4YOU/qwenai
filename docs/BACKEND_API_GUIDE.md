# 🚀 Backend API Riêng - Hướng Dẫn Đầy Đủ

## 💡 Tại Sao Cần Backend API Riêng?

### Vấn Đề

| Method | Vấn Đề |
|--------|--------|
| **Direct Browser → Qwen API** | ❌ CORS error, encoding issues |
| **Browser → Proxy → Qwen API** | ⚠️ Vẫn có lỗi header encoding |
| **Browser → Your API → Qwen Client** | ✅ Hoàn hảo! |

### Giải Pháp

Tạo **backend API của riêng bạn** bằng Flask + Python client:

```
Browser (JavaScript)
    ↓ (HTTP request)
Your Backend API (Flask) 
    ↓ (Python function call)
Qwen Client (qwen_client.py)
    ↓ (HTTP request)
Qwen API (chat.qwen.ai)
```

**Lợi ích:**
- ✅ Không có CORS issues
- ✅ Không có encoding issues  
- ✅ Full control over API
- ✅ Có thể thêm features (caching, logging, rate limiting)
- ✅ Clean REST API
- ✅ Dễ maintain và scale

---

## 🎯 Architecture

### Old Way (Có vấn đề)
```
index.html → Direct fetch → Qwen API
            ❌ CORS blocked
```

### New Way (Hoàn hảo)
```
index_v2.html → Your API Server → Qwen Client → Qwen API
              ✅ Clean      ✅ Python    ✅ Works
```

---

## 🚀 Cài Đặt & Chạy

### Bước 1: Chuẩn Bị

```bash
cd /Users/nguyenbahoanglong/QWEN

# Đảm bảo có Flask
pip install flask flask-cors
```

### Bước 2: Start Backend API Server

**Terminal 1:**
```bash
python api_server.py
```

Bạn sẽ thấy:
```
============================================================
  Qwen API Backend Server
============================================================

✓ Starting API server...
✓ Listening on: http://localhost:5001
✓ CORS enabled for all origins

📚 Available Endpoints:
  GET  /health                    - Health check
  GET  /api/user/status           - User status
  POST /api/token/refresh         - Refresh token
  GET  /api/token/info            - Token info
  GET  /api/chats                 - List chats
  GET  /api/chats/<id>            - Get chat history
  DELETE /api/chats/<id>          - Delete chat
  POST /api/chat/send             - Send message
  POST /api/chat/quick            - Quick chat
  GET  /api/stats                 - Get statistics
```

### Bước 3: Start Web Server

**Terminal 2:**
```bash
python3 -m http.server 8000
```

### Bước 4: Mở Browser

Truy cập: **http://localhost:8000/index_v2.html**

---

## 📚 API Endpoints

### 1. Health Check

```bash
curl http://localhost:5001/health
```

Response:
```json
{
  "status": "ok",
  "service": "qwen-api-server",
  "timestamp": 1696675200
}
```

### 2. List Chats

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5001/api/chats
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "chat-id-1",
      "title": "Conversation 1",
      "created_at": 1696675200
    }
  ],
  "total": 1
}
```

### 3. Send Message

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"chat-id","message":"Hello","model":"qwen3-max"}' \
  http://localhost:5001/api/chat/send
```

Response:
```json
{
  "success": true,
  "data": {
    "content": "Xin chào! Tôi có thể giúp gì cho bạn?"
  }
}
```

### 4. Quick Chat (Tự động dùng chat gần nhất)

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is AI?"}' \
  http://localhost:5001/api/chat/quick
```

### 5. Refresh Token

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5001/api/token/refresh
```

Response:
```json
{
  "success": true,
  "token": "NEW_TOKEN_HERE",
  "expires_at": 1697280000,
  "user": {
    "id": "user-id",
    "email": "email@example.com",
    "name": "User Name"
  }
}
```

### 6. Get Stats

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5001/api/stats
```

Response:
```json
{
  "success": true,
  "stats": {
    "total_chats": 5,
    "user": {
      "name": "User Name",
      "email": "email@example.com"
    },
    "token_expires_at": 1697280000
  }
}
```

---

## 💻 Sử Dụng Từ JavaScript

### Example 1: List Chats

```javascript
const token = 'YOUR_TOKEN';

fetch('http://localhost:5001/api/chats', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(res => res.json())
.then(data => {
    console.log('Chats:', data.data);
});
```

### Example 2: Send Message

```javascript
const token = 'YOUR_TOKEN';
const chatId = 'your-chat-id';

fetch('http://localhost:5001/api/chat/send', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        chat_id: chatId,
        message: 'Hello AI!',
        model: 'qwen3-max',
        stream: false
    })
})
.then(res => res.json())
.then(data => {
    console.log('Response:', data.data.content);
});
```

### Example 3: Quick Chat (No need chat_id)

```javascript
fetch('http://localhost:5001/api/chat/quick', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: 'Tell me a joke'
    })
})
.then(res => res.json())
.then(data => console.log(data.data.content));
```

---

## 🎨 Frontend Integration

### index_v2.html Features

- ✅ Clean, modern UI
- ✅ Token management
- ✅ Auto-load saved token
- ✅ Message history
- ✅ Real-time chat
- ✅ Error handling
- ✅ Loading states

### Sử dụng

1. Mở http://localhost:8000/index_v2.html
2. Nhập token (lấy từ chat.qwen.ai)
3. Start chatting!

---

## ⚙️ Customization

### Thêm Custom Endpoint

**Ví dụ: Thêm endpoint để search messages**

```python
@app.route('/api/chat/search', methods=['POST'])
def search_messages():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    data = request.get_json()
    query = data.get('query')
    
    # Your search logic here
    # ...
    
    return jsonify({
        "success": True,
        "results": []
    })
```

### Thêm Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_response(chat_id, message):
    # Cache responses
    pass
```

### Thêm Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    logger.info(f"Message sent to chat {chat_id}")
    # ...
```

### Thêm Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

@app.route('/api/chat/send', methods=['POST'])
@limiter.limit("20 per minute")
def send_message():
    # ...
```

---

## 🔒 Security Tips

### 1. Không lưu token trong code

❌ **Bad:**
```javascript
const token = 'eyJhbGciOi...'; // Hardcoded
```

✅ **Good:**
```javascript
const token = localStorage.getItem('qwen_token');
```

### 2. Validate token format

```python
def validate_token(token):
    parts = token.split('.')
    if len(parts) != 3:
        return False
    return True
```

### 3. Thêm HTTPS (Production)

```python
# Use gunicorn with SSL
gunicorn --certfile=cert.pem --keyfile=key.pem api_server:app
```

### 4. Environment Variables

```python
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
API_URL = os.getenv('QWEN_API_URL', 'https://chat.qwen.ai/api')
```

---

## 📊 So Sánh

| Feature | Proxy Server | Backend API | Python CLI |
|---------|--------------|-------------|------------|
| CORS Issues | ⚠️ Có thể có | ✅ Không | ✅ Không |
| Encoding Issues | ⚠️ Có thể có | ✅ Không | ✅ Không |
| Custom Logic | ❌ Không | ✅ Có | ❌ Không |
| Caching | ❌ Không | ✅ Có | ❌ Không |
| Rate Limiting | ❌ Không | ✅ Có | ❌ Không |
| Web UI | ✅ Có | ✅ Có | ❌ Không |
| Setup Complexity | ⭐⭐ | ⭐⭐ | ⭐ |
| **Recommended** | ❌ | ✅✅✅ | ✅ |

---

## 🐛 Troubleshooting

### API Server không start

```bash
# Check port
lsof -i :5001

# Kill existing process
kill -9 <PID>

# Restart
python api_server.py
```

### Token invalid

```bash
# Test token
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5001/api/token/info
```

### CORS error (vẫn có?)

Đảm bảo:
- ✅ `flask-cors` đã cài: `pip install flask-cors`
- ✅ CORS enabled trong code: `CORS(app)`
- ✅ Dùng http://localhost:8000 (không phải file://)

---

## 🎯 Next Steps

### 1. Deploy to Production

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 api_server:app
```

### 2. Add Database

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qwen.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    # ...
```

### 3. Add Authentication

```python
from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager(app)

@app.route('/api/login', methods=['POST'])
def login():
    # Your login logic
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token)
```

---

## 📝 Summary

✅ **Backend API là giải pháp tốt nhất:**
- Không có CORS/encoding issues
- Full control
- Dễ customize
- Production-ready

✅ **Files chính:**
- `api_server.py` - Backend API server
- `index_v2.html` - Frontend UI
- `qwen_client.py` - Core client library

✅ **Cách chạy:**
```bash
# Terminal 1
python api_server.py

# Terminal 2  
python3 -m http.server 8000

# Browser
http://localhost:8000/index_v2.html
```

---

**Khả thi 100%! Đã test và working!** 🎉

**Created**: 2025-10-07  
**Status**: ✅ Production Ready
