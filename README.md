# 🤖 Qwen Personal API

> Transform Qwen AI into your personal API with full control, no rate limits, and advanced features.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/qwen-api)

## ✨ Features

- ✅ **19 AI Models** - From Qwen3-Max to specialized coding/vision models
- ✅ **Thinking Mode** - See AI's reasoning process (perfect for complex problems)
- ✅ **Internet Search** - Get latest information with source citations
- ✅ **System Prompts** - Custom instructions to guide AI behavior
- ✅ **Vietnamese Support** - Full UTF-8 encoding for Vietnamese text
- ✅ **RESTful API** - Clean, simple endpoints
- ✅ **No Code Updates for Token** - Update token via API without redeploying
- ✅ **Free & Fast** - Use your Qwen account, no additional costs

## 🚀 Quick Start

### 1. Get Your Token

```bash
# Go to chat.qwen.ai
# Press F12 → Application → Cookies → copy 'token' value
```

### 2. Deploy to Vercel

```bash
# Fork this repo, then:
vercel

# Set environment variables:
vercel env add QWEN_TOKEN production     # Your token
vercel env add ADMIN_KEY production       # Random secure string

# Deploy:
vercel --prod
```

### 3. Use Your API

```bash
curl -X POST https://your-app.vercel.app/api/chat/quick \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

**That's it!** 🎉

## 📖 API Documentation

See [API_DOCS.md](./API_DOCS.md) for complete API reference.

### Quick Examples

**Simple Chat:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "What is Python?"}'
```

**With Thinking Mode:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "message": "Solve: 5 people shake hands once each, how many handshakes?",
    "thinking_enabled": true
  }'
```

**With Internet Search:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "message": "Latest AI news today",
    "search_enabled": true
  }'
```

**Choose Model:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "message": "Write Python hello world",
    "model": "qwen3-coder"
  }'
```

## 🔧 All Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/models` | GET | List all 19 models |
| `/api/chat/quick` | POST | Quick chat (auto-select chat) |
| `/api/chat/send` | POST | Send to specific chat |
| `/api/chats` | GET | List all chats |
| `/api/admin/token` | POST | Update token (no redeploy!) |

## 🎯 Available Models

| Model | Best For | Speed |
|-------|----------|-------|
| `qwen3-max` | General purpose (recommended) | ⭐⭐⭐ |
| `qwen3-coder` | Code generation | ⭐⭐⭐⭐ |
| `qwen3-vl-plus` | Vision + Thinking | ⭐⭐ |
| `qwen3-omni-flash` | Fast responses | ⭐⭐⭐⭐⭐ |
| `qwq-32b` | Complex reasoning | ⭐⭐⭐ |
| `qwen2.5-14b-instruct-1m` | Long documents (1M context!) | ⭐⭐⭐ |

[See all 19 models →](./docs/MODELS_GUIDE.md)

## 💡 Use Cases

### Personal AI Assistant
```python
import requests

API = "https://your-api.vercel.app"
TOKEN = "your-token"

def ask(question):
    response = requests.post(
        f"{API}/api/chat/quick",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"message": question}
    )
    return response.json()["data"]["content"]

print(ask("What's the weather like?"))
```

### Coding Assistant
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "message": "Write a binary search in Python",
    "model": "qwen3-coder",
    "system_prompt": "You are a Python expert. Always include type hints and docstrings."
  }'
```

### Research Tool
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "message": "Summarize latest quantum computing breakthroughs 2025",
    "thinking_enabled": true,
    "search_enabled": true
  }'
```

## 🔐 Token Management

### When Token Expires (7 days)

**Option 1: Via API (5 seconds, no redeploy!)**
```bash
curl -X POST https://your-api.vercel.app/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "NEW_TOKEN_FROM_BROWSER",
    "admin_key": "YOUR_ADMIN_KEY"
  }'
```

**Option 2: Via Vercel Dashboard (30 seconds)**
1. Vercel Dashboard → Your Project
2. Settings → Environment Variables
3. Edit `QWEN_TOKEN` → Save
4. Redeploy

[Learn more →](./docs/VERCEL_DEPLOY.md)

## 📁 Project Structure

```
qwen-api/
├── api_server.py          # Main API server
├── qwen_client.py         # Qwen API wrapper
├── simple_client.py       # Simplified Python client
├── index_v2.html          # Web UI
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel configuration
├── API_DOCS.md            # Complete API documentation
├── DEPLOY.md              # Deployment guide
│
├── docs/                  # Detailed guides
│   ├── MODELS_GUIDE.md
│   ├── THINKING_AND_SEARCH.md
│   ├── SYSTEM_PROMPT_COMPLETE.md
│   └── VERCEL_DEPLOY.md
│
├── tests/                 # Test scripts
│   └── test_*.py
│
└── examples/              # Example usage
    └── index.html
```

## 🐍 Python Client

```python
from simple_client import ask

# One-liner usage
print(ask("What is Python?"))
print(ask("Write code", model="qwen3-coder"))
print(ask("Latest news", search=True))
print(ask("Solve math problem", thinking=True))
```

[Python client docs →](./simple_client.py)

## 🌐 Web Interface

Open `index_v2.html` for a beautiful web UI with:
- Model selector
- System prompt editor
- Thinking & search toggles
- Chat history
- Token management

## 🔒 Security

- ✅ Admin key protects token update endpoint
- ✅ Token stored securely (not in code)
- ✅ CORS configured
- ✅ No sensitive data in git

**Important:** Keep your `ADMIN_KEY` secret! Never commit `.env` files.

## 📊 Performance

| Operation | Response Time |
|-----------|---------------|
| Simple query | 2-3s |
| With thinking | 4-6s |
| With search | 5-8s |
| Both features | 8-12s |

## 🆚 Why This vs Official API?

| Feature | This Project | Official API |
|---------|--------------|--------------|
| Cost | Free (use your account) | Paid |
| Rate Limits | None | Yes |
| Models | 19 models | Limited |
| Thinking Mode | ✅ | ❌ |
| Internet Search | ✅ | ❌ |
| Custom Prompts | ✅ | Limited |
| Control | Full | Limited |

## 📚 Documentation

- **[API_DOCS.md](./API_DOCS.md)** - Complete API reference
- **[DEPLOY.md](./DEPLOY.md)** - Deployment guide
- **[docs/MODELS_GUIDE.md](./docs/MODELS_GUIDE.md)** - All 19 models
- **[docs/THINKING_AND_SEARCH.md](./docs/THINKING_AND_SEARCH.md)** - Advanced features
- **[docs/SYSTEM_PROMPT_COMPLETE.md](./docs/SYSTEM_PROMPT_COMPLETE.md)** - System prompts guide

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## ⚠️ Disclaimer

This project uses the Qwen web interface API. Use responsibly and respect Qwen's terms of service.

## 🙏 Acknowledgments

- Qwen AI by Alibaba Cloud
- Built with Flask, Python, and modern web technologies

---

**Made with ❤️ for the AI community**

Star ⭐ this repo if you find it useful!
