# 📖 API Documentation

Complete API reference for Qwen Personal API.

**Base URL:** `https://your-app.vercel.app`

---

## 🔐 Authentication

All endpoints require JWT token in Authorization header:

```bash
Authorization: Bearer YOUR_QWEN_TOKEN
```

**Get token:** `chat.qwen.ai` → F12 → Application → Cookies → `token`

---

## 📋 Table of Contents

- [Health & Status](#health--status)
- [Chat Endpoints](#chat-endpoints)
- [Model Management](#model-management)
- [Admin Endpoints](#admin-endpoints)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

---

## Health & Status

### GET `/health`

Health check endpoint.

**Request:**
```bash
curl https://your-api.vercel.app/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "qwen-api-server",
  "timestamp": 1759825000
}
```

---

## Chat Endpoints

### POST `/api/chat/quick`

Quick chat - automatically uses most recent chat.

**Best for:** Simple usage, no chat_id management needed.

**Request:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "model": "qwen3-max",
    "system_prompt": "You are a helpful assistant",
    "thinking_enabled": false,
    "search_enabled": false
  }'
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `message` | string | ✅ Yes | - | Your message |
| `model` | string | ❌ No | `qwen3-max` | Model ID |
| `system_prompt` | string | ❌ No | null | Custom instructions |
| `thinking_enabled` | boolean | ❌ No | false | Enable thinking mode |
| `search_enabled` | boolean | ❌ No | false | Enable internet search |

**Response:**
```json
{
  "success": true,
  "chat_id": "93cee988-4875-42db-...",
  "data": {
    "content": "Hello! How can I help you today?",
    "thinking": "User greeted me..." // Only if thinking_enabled=true
  }
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing message)
- `401` - Unauthorized (invalid token)
- `404` - No chats found (create one first)
- `500` - Server error

---

### POST `/api/chat/send`

Send message to specific chat.

**Best for:** When you need precise chat control.

**Request:**
```bash
curl -X POST https://your-api.vercel.app/api/chat/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "93cee988-4875-42db-...",
    "message": "Explain Python decorators",
    "model": "qwen3-max",
    "system_prompt": "Explain like I am 5",
    "thinking_enabled": false,
    "search_enabled": false
  }'
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `chat_id` | string | ✅ Yes | - | Chat conversation ID |
| `message` | string | ✅ Yes | - | Your message |
| `model` | string | ❌ No | `qwen3-max` | Model ID |
| `system_prompt` | string | ❌ No | null | Custom instructions |
| `thinking_enabled` | boolean | ❌ No | false | Enable thinking mode |
| `search_enabled` | boolean | ❌ No | false | Enable internet search |

**Response:**
```json
{
  "success": true,
  "data": {
    "content": "Python decorators are functions that...",
    "thinking": "..." // Optional
  }
}
```

---

### GET `/api/chats`

List all chat conversations.

**Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-api.vercel.app/api/chats?page=1
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `page` | integer | ❌ No | 1 | Page number |

**Response:**
```json
{
  "data": [
    {
      "id": "93cee988-4875-42db-...",
      "name": "New Chat",
      "created_at": 1759800000,
      "updated_at": 1759825000,
      "message_count": 15
    }
  ],
  "pagination": {
    "page": 1,
    "total": 5
  }
}
```

---

### GET `/api/chats/<chat_id>`

Get chat history.

**Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-api.vercel.app/api/chats/93cee988-4875-42db-...
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "93cee988-4875-42db-...",
    "messages": [
      {
        "id": "msg-1",
        "role": "user",
        "content": "Hello!",
        "timestamp": 1759825000
      },
      {
        "id": "msg-2",
        "role": "assistant",
        "content": "Hi! How can I help?",
        "timestamp": 1759825002
      }
    ]
  }
}
```

---

### DELETE `/api/chats/<chat_id>`

Delete a chat conversation.

**Request:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-api.vercel.app/api/chats/93cee988-4875-42db-...
```

**Response:**
```json
{
  "success": true,
  "message": "Chat deleted successfully"
}
```

---

## Model Management

### GET `/api/models`

List all available models.

**Request:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-api.vercel.app/api/models
```

**Response:**
```json
{
  "data": [
    {
      "id": "qwen3-max",
      "name": "Qwen3-Max",
      "object": "model",
      "owned_by": "qwen",
      "info": {
        "description": "Most advanced model in Qwen series...",
        "capabilities": {
          "vision": true,
          "document": true,
          "video": true,
          "audio": true,
          "citations": true
        },
        "max_context_length": 262144,
        "max_generation_length": 32768
      }
    },
    // ... 18 more models
  ]
}
```

**Model IDs:**
- `qwen3-max` - Best all-around (recommended)
- `qwen3-coder` - Coding specialist
- `qwen3-vl-plus` - Vision + Thinking
- `qwen3-omni-flash` - Fast responses
- `qwen2.5-turbo` - Fast text
- `qwq-32b` - Reasoning specialist
- `qwen2.5-14b-instruct-1m` - 1M context!
- [See all 19 models →](./docs/MODELS_GUIDE.md)

---

## Admin Endpoints

### POST `/api/admin/token`

Update server token without redeployment.

**⚠️ Requires:** `admin_key` (set in environment variables)

**Request:**
```bash
curl -X POST https://your-api.vercel.app/api/admin/token \
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
  "message": "Token updated successfully",
  "timestamp": 1759825000
}
```

**Status Codes:**
- `200` - Success
- `400` - Missing token
- `403` - Invalid admin key
- `500` - Server error

**Usage:**
When your Qwen token expires (after 7 days):
1. Get new token from browser
2. Call this endpoint
3. Done! No redeployment needed.

---

### GET `/api/admin/token`

Check stored token (masked for security).

**Request:**
```bash
curl "https://your-api.vercel.app/api/admin/token?admin_key=YOUR_KEY"
```

**Response:**
```json
{
  "has_token": true,
  "token_preview": "eyJhbGciOiJIUzI1Ni...oken_12345"
}
```

---

## Error Handling

All endpoints return consistent error format:

```json
{
  "error": "Error message here"
}
```

**Common Errors:**

| Status | Error | Solution |
|--------|-------|----------|
| 400 | `message is required` | Include message in body |
| 401 | `No authorization token` | Add Authorization header |
| 401 | `Invalid token` | Get new token from browser |
| 403 | `Invalid admin key` | Check ADMIN_KEY env var |
| 404 | `No chats found` | Create a chat first |
| 500 | Various server errors | Check logs, retry |

---

## Rate Limits

**None!** This uses your personal Qwen account, so:
- ✅ No rate limits
- ✅ Free usage
- ✅ Same limits as web interface

---

## Examples

### Python

```python
import requests

API_BASE = "https://your-api.vercel.app"
TOKEN = "your-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Simple chat
response = requests.post(
    f"{API_BASE}/api/chat/quick",
    headers=headers,
    json={"message": "Hello!"}
)
print(response.json()["data"]["content"])

# With features
response = requests.post(
    f"{API_BASE}/api/chat/quick",
    headers=headers,
    json={
        "message": "Analyze AI trends 2025",
        "model": "qwen3-max",
        "thinking_enabled": True,
        "search_enabled": True
    }
)
data = response.json()
print("Thinking:", data["data"].get("thinking", "N/A"))
print("Answer:", data["data"]["content"])
```

### JavaScript/Node.js

```javascript
const API_BASE = "https://your-api.vercel.app";
const TOKEN = "your-token";

async function chat(message, options = {}) {
  const response = await fetch(`${API_BASE}/api/chat/quick`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message,
      ...options
    })
  });
  
  const data = await response.json();
  return data.data.content;
}

// Usage
chat("What is Python?").then(console.log);

chat("Latest AI news", { search_enabled: true }).then(console.log);

chat("Solve math problem", { thinking_enabled: true }).then(console.log);
```

### cURL

```bash
# Simple
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Hello"}'

# With thinking
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Complex problem", "thinking_enabled": true}'

# With search
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Latest news", "search_enabled": true}'

# With model
curl -X POST https://your-api.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Write code", "model": "qwen3-coder"}'
```

---

## Advanced Features

### System Prompts

Guide AI behavior with custom instructions:

```json
{
  "message": "Explain quantum computing",
  "system_prompt": "You are a physics professor. Explain concepts clearly with examples. Use simple language."
}
```

**Examples:**
- **Concise:** `"Reply in maximum 2 sentences"`
- **Expert:** `"You are a Python expert. Always include type hints and docstrings."`
- **Teacher:** `"Explain like I'm 5 years old"`
- **Format:** `"Always respond in JSON format"`

[See full guide →](./docs/SYSTEM_PROMPT_COMPLETE.md)

### Thinking Mode

See AI's reasoning process:

```json
{
  "message": "If 5 people shake hands once each, how many total handshakes?",
  "thinking_enabled": true
}
```

**Response includes:**
```json
{
  "thinking": "Let me think... Person A shakes with B,C,D,E = 4 handshakes...",
  "content": "Total: 10 handshakes. Formula: n(n-1)/2"
}
```

**Best for:**
- Math problems
- Logic puzzles
- Complex reasoning
- Algorithm design

[See full guide →](./docs/THINKING_AND_SEARCH.md)

### Internet Search

Get latest information:

```json
{
  "message": "Latest AI breakthroughs 2025",
  "search_enabled": true
}
```

**Response includes citations:**
```
According to recent reports [[1]][[2]], major breakthroughs include...

[1] "OpenAI announces GPT-5..."
[2] "Google releases Gemini 2.0..."
```

**Best for:**
- Current events
- Latest news
- Real-time data
- Trends analysis

[See full guide →](./docs/THINKING_AND_SEARCH.md)

---

## Best Practices

### 1. Choose Right Model

```python
# General → qwen3-max
# Coding → qwen3-coder  
# Speed → qwen3-omni-flash
# Reasoning → qwen3-vl-plus with thinking=True
# Long docs → qwen2.5-14b-instruct-1m
```

### 2. Use System Prompts

```python
system_prompt = """
Role: Senior Python Developer
Task: Review code and suggest improvements
Format: 
  1. Issues found
  2. Suggestions
  3. Improved code
Constraints: Keep explanations concise
"""
```

### 3. Enable Features Strategically

```python
# Only enable thinking for complex problems
thinking = is_math_or_logic(message)

# Only enable search for current events
search = needs_latest_info(message)
```

### 4. Handle Errors Gracefully

```python
try:
    response = requests.post(...)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        # Token expired - refresh it
    elif e.response.status_code == 404:
        # No chats - create one
```

---

## Performance Tips

1. **Use `/api/chat/quick`** for simplicity (no chat_id management)
2. **Cache model list** (rarely changes)
3. **Disable features you don't need** (faster response)
4. **Use `qwen3-omni-flash` for speed**
5. **Set reasonable timeouts** (30s recommended)

---

## Webhook Support (Coming Soon)

Subscribe to events:
- Message received
- Response ready
- Token expiring soon

---

## Support

- **Issues:** GitHub Issues
- **Docs:** [Complete documentation](./docs/)
- **Examples:** [Example code](./examples/)

---

**Last Updated:** 2025-10-07  
**API Version:** 2.0  
**Status:** ✅ Production Ready
