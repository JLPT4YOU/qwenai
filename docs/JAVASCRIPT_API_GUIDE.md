# 📘 Qwen API - Hướng Dẫn JavaScript Chi Tiết

## 🔐 Token Management

### Token có thể bị reset/hết hạn

**⚠️ Quan trọng**: JWT Token của Qwen **có thời hạn** (thường vài ngày đến vài tuần).

```javascript
// Token structure (decoded)
{
  "id": "user-uuid",
  "last_password_change": 1759815466,
  "exp": 1760420288  // ← Thời gian hết hạn (Unix timestamp)
}
```

**Khi nào token hết hạn?**
- Sau một khoảng thời gian nhất định (thường 7-30 ngày)
- Khi user đổi password
- Khi logout khỏi tất cả devices
- Khi Qwen update security

**Giải pháp:**
- Lưu token trong localStorage/cookie
- Check token expiration trước khi dùng
- Có UI để user nhập token mới
- Auto-detect và yêu cầu refresh khi 401 Unauthorized

---

## 🚀 Thiết Lập Ban Đầu

### 1. Lấy Token

```javascript
// Cách 1: Lấy từ browser
// 1. Truy cập: https://chat.qwen.ai
// 2. Đăng nhập
// 3. F12 → Application → Local Storage → chat.qwen.ai
// 4. Copy value của key "token"

// Cách 2: Extract từ JavaScript (nếu đang ở trang Qwen)
const token = localStorage.getItem('token');
console.log('Token:', token);
```

### 2. Setup Base Configuration

```javascript
// config.js
const QWEN_CONFIG = {
    baseURL: 'https://chat.qwen.ai/api',
    version: 'v2',
    defaultModel: 'qwen3-max',
    timeout: 30000,
    maxRetries: 3
};

// Lưu token
function saveToken(token) {
    localStorage.setItem('qwen_auth_token', token);
}

// Lấy token
function getToken() {
    return localStorage.getItem('qwen_auth_token');
}

// Check token expiration
function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        return Date.now() >= exp;
    } catch (e) {
        return true;
    }
}

// Get token info
function getTokenInfo(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return {
            userId: payload.id,
            expiresAt: new Date(payload.exp * 1000),
            daysRemaining: Math.floor((payload.exp * 1000 - Date.now()) / (1000 * 60 * 60 * 24))
        };
    } catch (e) {
        return null;
    }
}
```

---

## 🔧 Core API Functions

### 1. Helper Functions

```javascript
// Generate UUID v4
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Create headers
function createHeaders(token) {
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    };
}

// Create streaming headers
function createStreamingHeaders(token) {
    return {
        ...createHeaders(token),
        'Accept': 'text/event-stream',
        'x-accel-buffering': 'no',
        'source': 'web'
    };
}

// Handle API errors
function handleApiError(response, data) {
    if (!response.ok) {
        const errorMsg = data?.data?.details || data?.detail || 'Unknown error';
        throw new Error(`API Error (${response.status}): ${errorMsg}`);
    }
}
```

### 2. User Status

```javascript
// Check user status
async function getUserStatus(token) {
    const response = await fetch(`${QWEN_CONFIG.baseURL}/v2/users/status`, {
        headers: createHeaders(token)
    });
    
    const data = await response.json();
    handleApiError(response, data);
    
    return data.data; // true/false
}

// Get user settings
async function getUserSettings(token) {
    const response = await fetch(`${QWEN_CONFIG.baseURL}/v2/users/user/settings`, {
        headers: createHeaders(token)
    });
    
    const data = await response.json();
    handleApiError(response, data);
    
    return data.data;
}
```

### 3. Chat Management

```javascript
// List all chats
async function listChats(token, page = 1) {
    const response = await fetch(
        `${QWEN_CONFIG.baseURL}/v2/chats/?page=${page}`,
        { headers: createHeaders(token) }
    );
    
    const data = await response.json();
    handleApiError(response, data);
    
    return data.data; // Array of chats
}

// Get chat details and history
async function getChatHistory(token, chatId) {
    const response = await fetch(
        `${QWEN_CONFIG.baseURL}/v2/chats/${chatId}`,
        { headers: createHeaders(token) }
    );
    
    const data = await response.json();
    handleApiError(response, data);
    
    return data.data;
}

// Get pinned chats
async function getPinnedChats(token) {
    const response = await fetch(
        `${QWEN_CONFIG.baseURL}/v2/chats/pinned`,
        { headers: createHeaders(token) }
    );
    
    const data = await response.json();
    handleApiError(response, data);
    
    return data.data;
}

// Delete chat
async function deleteChat(token, chatId) {
    const response = await fetch(
        `${QWEN_CONFIG.baseURL}/v2/chats/${chatId}`,
        {
            method: 'DELETE',
            headers: createHeaders(token)
        }
    );
    
    return response.ok;
}
```

### 4. Send Message (Streaming)

```javascript
// Send message with streaming response
async function sendMessage(token, chatId, message, options = {}) {
    const {
        model = 'qwen3-max',
        parentId = null,
        onChunk = null,
        onComplete = null,
        onError = null
    } = options;
    
    try {
        // Get parent_id from chat history if not provided
        let actualParentId = parentId;
        if (!actualParentId) {
            const history = await getChatHistory(token, chatId);
            actualParentId = history.currentId || generateUUID();
        }
        
        // Build payload
        const fid = generateUUID();
        const timestamp = Math.floor(Date.now() / 1000);
        
        const payload = {
            stream: true,
            incremental_output: true,
            chat_id: chatId,
            chat_mode: "normal",
            model: model,
            parent_id: actualParentId,
            messages: [{
                fid: fid,
                parentId: actualParentId,
                childrenIds: [],
                role: "user",
                content: message,
                user_action: "chat",
                files: [],
                timestamp: timestamp,
                models: [model],
                chat_type: "t2t",
                feature_config: {
                    thinking_enabled: false,
                    output_schema: "phase"
                },
                extra: {
                    meta: {
                        subChatType: "t2t"
                    }
                },
                sub_chat_type: "t2t",
                parent_id: actualParentId
            }],
            timestamp: timestamp
        };
        
        // Send request
        const response = await fetch(
            `${QWEN_CONFIG.baseURL}/v2/chat/completions?chat_id=${chatId}`,
            {
                method: 'POST',
                headers: createStreamingHeaders(token),
                body: JSON.stringify(payload)
            }
        );
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.data?.details || 'Request failed');
        }
        
        // Handle streaming
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data:')) {
                    const data = line.substring(5).trim();
                    
                    if (data === '[DONE]') {
                        if (onComplete) onComplete(fullResponse);
                        continue;
                    }
                    
                    try {
                        const json = JSON.parse(data);
                        
                        // Extract content from different response formats
                        const content = json.output?.text || 
                                      json.choices?.[0]?.delta?.content || 
                                      json.content || '';
                        
                        if (content) {
                            fullResponse = content;
                            if (onChunk) onChunk(content);
                        }
                    } catch (e) {
                        // Skip invalid JSON
                    }
                }
            }
        }
        
        return fullResponse;
        
    } catch (error) {
        if (onError) onError(error);
        throw error;
    }
}

// Send message without streaming
async function sendMessageSync(token, chatId, message, model = 'qwen3-max') {
    return new Promise((resolve, reject) => {
        let fullResponse = '';
        
        sendMessage(token, chatId, message, {
            model,
            onChunk: (content) => {
                fullResponse = content;
            },
            onComplete: (content) => {
                resolve(content);
            },
            onError: (error) => {
                reject(error);
            }
        });
    });
}
```

---

## 💬 Usage Examples

### Example 1: Simple Chat

```javascript
// Initialize
const token = getToken();

if (!token || isTokenExpired(token)) {
    alert('Token expired! Please login again.');
    // Redirect to token input
}

// Get chat list
const chats = await listChats(token);
const chatId = chats[0].id;

// Send message
const response = await sendMessageSync(
    token,
    chatId,
    "What is the capital of Vietnam?"
);

console.log('AI Response:', response);
```

### Example 2: Streaming Chat

```javascript
const token = getToken();
const chats = await listChats(token);
const chatId = chats[0].id;

// Display element
const responseDiv = document.getElementById('ai-response');

await sendMessage(token, chatId, "Tell me a story", {
    model: 'qwen3-max',
    
    onChunk: (content) => {
        // Update UI in real-time
        responseDiv.textContent = content;
        console.log('Streaming:', content);
    },
    
    onComplete: (fullContent) => {
        console.log('Complete:', fullContent);
        // Save to history, etc.
    },
    
    onError: (error) => {
        console.error('Error:', error);
        responseDiv.textContent = `Error: ${error.message}`;
    }
});
```

### Example 3: Chat Manager Class

```javascript
class QwenChatManager {
    constructor(token) {
        this.token = token;
        this.currentChatId = null;
    }
    
    async initialize() {
        // Check token
        if (isTokenExpired(this.token)) {
            throw new Error('Token expired');
        }
        
        // Get chats
        const chats = await listChats(this.token);
        if (chats.length > 0) {
            this.currentChatId = chats[0].id;
        } else {
            throw new Error('No chats found. Please create one on chat.qwen.ai');
        }
        
        return this;
    }
    
    async chat(message, callbacks = {}) {
        if (!this.currentChatId) {
            throw new Error('Not initialized');
        }
        
        return await sendMessage(
            this.token,
            this.currentChatId,
            message,
            callbacks
        );
    }
    
    async getHistory() {
        return await getChatHistory(this.token, this.currentChatId);
    }
    
    async switchChat(chatId) {
        this.currentChatId = chatId;
    }
}

// Usage
const manager = new QwenChatManager(getToken());
await manager.initialize();

await manager.chat("Hello!", {
    onChunk: (text) => console.log('>', text),
    onComplete: (text) => console.log('Done:', text)
});
```

### Example 4: Multi-turn Conversation

```javascript
async function conversation(token, chatId, questions) {
    for (const question of questions) {
        console.log(`\n🧑 You: ${question}`);
        console.log('🤖 AI: ', '');
        
        await sendMessage(token, chatId, question, {
            onChunk: (content) => {
                process.stdout.write('\r🤖 AI: ' + content);
            },
            onComplete: () => {
                console.log('\n');
            }
        });
        
        // Wait a bit between messages
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

// Usage
const questions = [
    "My name is Alice",
    "What's my name?",
    "Tell me about yourself"
];

await conversation(token, chatId, questions);
```

---

## 🎨 UI Integration Examples

### Example: React Component

```javascript
import { useState, useEffect } from 'react';

function QwenChat() {
    const [token, setToken] = useState(localStorage.getItem('qwen_token'));
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [chatId, setChatId] = useState(null);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        if (token) {
            initChat();
        }
    }, [token]);
    
    async function initChat() {
        const chats = await listChats(token);
        if (chats.length > 0) {
            setChatId(chats[0].id);
        }
    }
    
    async function handleSend() {
        if (!input.trim() || !chatId) return;
        
        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);
        
        let aiMsg = { role: 'assistant', content: '' };
        setMessages(prev => [...prev, aiMsg]);
        
        await sendMessage(token, chatId, input, {
            onChunk: (content) => {
                setMessages(prev => {
                    const newMsgs = [...prev];
                    newMsgs[newMsgs.length - 1].content = content;
                    return newMsgs;
                });
            },
            onComplete: () => {
                setLoading(false);
            }
        });
    }
    
    return (
        <div className="chat">
            {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                    {msg.content}
                </div>
            ))}
            
            <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyPress={e => e.key === 'Enter' && handleSend()}
                disabled={loading}
            />
            
            <button onClick={handleSend} disabled={loading}>
                Send
            </button>
        </div>
    );
}
```

### Example: Vue Component

```javascript
<template>
  <div class="qwen-chat">
    <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
      {{ msg.content }}
    </div>
    
    <input 
      v-model="input" 
      @keyup.enter="send"
      :disabled="loading"
      placeholder="Type a message..."
    />
    
    <button @click="send" :disabled="loading">
      {{ loading ? 'Sending...' : 'Send' }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: localStorage.getItem('qwen_token'),
      chatId: null,
      messages: [],
      input: '',
      loading: false
    };
  },
  
  async mounted() {
    await this.initChat();
  },
  
  methods: {
    async initChat() {
      const chats = await listChats(this.token);
      if (chats.length > 0) {
        this.chatId = chats[0].id;
      }
    },
    
    async send() {
      if (!this.input.trim()) return;
      
      this.messages.push({
        id: Date.now(),
        role: 'user',
        content: this.input
      });
      
      const userInput = this.input;
      this.input = '';
      this.loading = true;
      
      const aiMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: ''
      };
      this.messages.push(aiMsg);
      
      await sendMessage(this.token, this.chatId, userInput, {
        onChunk: (content) => {
          aiMsg.content = content;
        },
        onComplete: () => {
          this.loading = false;
        }
      });
    }
  }
};
</script>
```

---

## ⚠️ Error Handling

```javascript
// Comprehensive error handler
async function safeApiCall(apiFunction, ...args) {
    try {
        return await apiFunction(...args);
    } catch (error) {
        if (error.message.includes('401')) {
            // Token expired
            console.error('Token expired. Please login again.');
            localStorage.removeItem('qwen_token');
            window.location.href = '/login';
        } else if (error.message.includes('404')) {
            console.error('Resource not found:', error.message);
        } else if (error.message.includes('429')) {
            console.error('Rate limit exceeded. Please wait.');
        } else {
            console.error('API Error:', error);
        }
        throw error;
    }
}

// Usage
try {
    const response = await safeApiCall(
        sendMessageSync,
        token,
        chatId,
        "Hello"
    );
} catch (error) {
    // Error already handled
}
```

---

## 🔄 Token Refresh Strategy

### **PHÁT HIỆN MỚI**: Auto-refresh Token! 🎉

Qwen API có endpoint để **tự động refresh token**:

```javascript
// Refresh token và lấy token mới
async function refreshToken(currentToken) {
    const response = await fetch('https://chat.qwen.ai/api/v1/auths/', {
        headers: {
            'Authorization': `Bearer ${currentToken}`,
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    
    // data includes:
    // - token: NEW token
    // - expires_at: Unix timestamp
    // - email, name, permissions, etc.
    
    if (data.token) {
        localStorage.setItem('qwen_token', data.token);
        console.log('✓ Token refreshed');
        console.log('Expires:', new Date(data.expires_at * 1000));
        return data.token;
    }
    
    return null;
}

// Usage
const newToken = await refreshToken(oldToken);
```

### Full Token Manager with Auto-Refresh

```javascript
// Auto-refresh token detection
class TokenManager {
    constructor() {
        this.token = localStorage.getItem('qwen_token');
        this.checkInterval = null;
    }
    
    startMonitoring() {
        // Check every hour
        this.checkInterval = setInterval(() => {
            this.checkTokenExpiry();
        }, 3600000);
        
        this.checkTokenExpiry();
    }
    
    checkTokenExpiry() {
        if (!this.token) return;
        
        const info = getTokenInfo(this.token);
        if (!info) return;
        
        if (info.daysRemaining <= 3) {
            this.showExpiryWarning(info.daysRemaining);
        }
        
        if (info.daysRemaining <= 0) {
            this.handleExpiredToken();
        }
    }
    
    showExpiryWarning(days) {
        console.warn(`⚠️ Token expires in ${days} days!`);
        // Show UI notification
    }
    
    handleExpiredToken() {
        console.error('❌ Token expired!');
        localStorage.removeItem('qwen_token');
        // Show token input modal
    }
    
    stopMonitoring() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
    }
}

// Usage
const tokenManager = new TokenManager();
tokenManager.startMonitoring();
```

---

## 📱 Complete Working Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Qwen Chat Demo</title>
    <style>
        /* Add your styles */
    </style>
</head>
<body>
    <div id="app">
        <div id="messages"></div>
        <input id="input" placeholder="Type a message...">
        <button onclick="send()">Send</button>
    </div>
    
    <script src="qwen-api.js"></script>
    <script>
        let chatId = null;
        const token = prompt('Enter your Qwen token:');
        
        if (token) {
            localStorage.setItem('qwen_token', token);
            init();
        }
        
        async function init() {
            const chats = await listChats(token);
            chatId = chats[0]?.id;
            console.log('Chat ID:', chatId);
        }
        
        async function send() {
            const input = document.getElementById('input');
            const msg = input.value.trim();
            if (!msg || !chatId) return;
            
            addMessage('user', msg);
            input.value = '';
            
            const aiDiv = addMessage('assistant', '');
            
            await sendMessage(token, chatId, msg, {
                onChunk: (content) => {
                    aiDiv.textContent = content;
                },
                onError: (error) => {
                    aiDiv.textContent = `Error: ${error.message}`;
                    aiDiv.style.color = 'red';
                }
            });
        }
        
        function addMessage(role, content) {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.textContent = content;
            document.getElementById('messages').appendChild(div);
            return div;
        }
    </script>
</body>
</html>
```

---

## 📊 API Reference Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v2/users/status` | GET | Check user status |
| `/v2/users/user/settings` | GET | Get user settings |
| `/v2/chats/?page={n}` | GET | List chats |
| `/v2/chats/{id}` | GET | Get chat history |
| `/v2/chats/{id}` | DELETE | Delete chat |
| `/v2/chats/pinned` | GET | Get pinned chats |
| `/v2/chat/completions?chat_id={id}` | POST | **Send message** |

---

## 🎓 Best Practices

1. **Always check token expiry** before API calls
2. **Handle errors gracefully** with user-friendly messages
3. **Use streaming** for better UX
4. **Store token securely** (not in plain text in production)
5. **Rate limit your requests** to avoid being blocked
6. **Cache chat list** to reduce API calls
7. **Implement retry logic** for failed requests

---

## 🔗 Resources

- **HTML Demo**: `index.html`
- **Python Client**: `qwen_client.py`
- **API Research**: `API_RESEARCH.md`
- **Quick Start**: `QUICK_START.md`

---

**Created**: 2025-10-07  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
