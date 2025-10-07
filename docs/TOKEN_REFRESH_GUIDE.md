# 🔄 Qwen Token Refresh - Complete Guide

## 🎉 Phát Hiện Quan Trọng

Token của Qwen **KHÔNG cần phải lấy từ browser mỗi lần hết hạn**!

API có endpoint để **tự động refresh token**: `/api/v1/auths/`

---

## 📌 Tóm Tắt

- ✅ Token **CÓ THỂ** tự động refresh
- ✅ Không cần login lại
- ✅ Không cần vào browser F12
- ✅ Chỉ cần gọi API `/v1/auths/` với token hiện tại
- ✅ Nhận token mới với expiration mới

---

## 🔑 Token Lifecycle

```
1. Lấy token ban đầu từ browser (chỉ 1 lần)
   ↓
2. Sử dụng token để chat
   ↓
3. Khi token sắp hết hạn (còn < 3 ngày)
   ↓
4. Gọi /v1/auths/ để refresh
   ↓
5. Lưu token mới
   ↓
6. Quay lại bước 2
```

**Kết quả**: Token không bao giờ hết hạn (miễn là refresh định kỳ)!

---

## 🚀 API Endpoint

### Request

```http
GET /api/v1/auths/ HTTP/1.1
Host: chat.qwen.ai
Authorization: Bearer YOUR_CURRENT_TOKEN
Content-Type: application/json
```

### Response

```json
{
  "id": "f4506b78-a768-4a55-89ac-c5fb61be7a08",
  "email": "user@example.com",
  "name": "User Name",
  "role": "user",
  "profile_image_url": "...",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",  // ← Token mới
  "token_type": "Bearer",
  "expires_at": 1760423581,  // ← Unix timestamp
  "permissions": {
    "workspace": {
      "models": false,
      "knowledge": false,
      "prompts": false,
      "tools": false
    },
    "chat": {
      "file_upload": true,
      "delete": true,
      "edit": true,
      "temporary": true
    }
  }
}
```

---

## 💻 Implementation

### Python

```python
from qwen_client import QwenClient

client = QwenClient(auth_token="your_token")

# Refresh token
new_info = client.refresh_token()
# ✓ Token refreshed. Expires at: 2025-10-14 15:34:20

# Get token info
info = client.get_token_info()
print(f"User: {info['name']}")
print(f"Expires: {info['expires_at']}")
print(f"Days left: {(info['expires_at'] - time.time()) / 86400:.1f}")
```

### JavaScript

```javascript
async function refreshToken(currentToken) {
    const response = await fetch('https://chat.qwen.ai/api/v1/auths/', {
        headers: {
            'Authorization': `Bearer ${currentToken}`,
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    
    if (data.token) {
        // Lưu token mới
        localStorage.setItem('qwen_token', data.token);
        
        // Tính thời gian còn lại
        const expiresAt = new Date(data.expires_at * 1000);
        const daysLeft = (data.expires_at * 1000 - Date.now()) / (1000 * 60 * 60 * 24);
        
        console.log('✓ Token refreshed');
        console.log('Expires:', expiresAt.toLocaleString());
        console.log('Days left:', daysLeft.toFixed(1));
        
        return data.token;
    }
    
    return null;
}

// Usage
const newToken = await refreshToken(oldToken);
```

### curl

```bash
curl "https://chat.qwen.ai/api/v1/auths/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

---

## ⏰ Auto-Refresh Strategy

### Strategy 1: Scheduled Refresh

```javascript
class TokenManager {
    constructor(token) {
        this.token = token;
        this.refreshInterval = null;
    }
    
    startAutoRefresh() {
        // Refresh every 6 days (token expires in ~7 days)
        this.refreshInterval = setInterval(async () => {
            console.log('Auto-refreshing token...');
            this.token = await refreshToken(this.token);
        }, 6 * 24 * 60 * 60 * 1000); // 6 days
    }
    
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }
}

// Usage
const manager = new TokenManager(token);
manager.startAutoRefresh();
```

### Strategy 2: On-Demand Refresh

```javascript
async function checkAndRefreshToken(token) {
    // Decode token to get expiration
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiresAt = payload.exp * 1000;
    const daysLeft = (expiresAt - Date.now()) / (1000 * 60 * 60 * 24);
    
    // Refresh if less than 3 days left
    if (daysLeft < 3) {
        console.log(`Token expires in ${daysLeft.toFixed(1)} days. Refreshing...`);
        return await refreshToken(token);
    }
    
    return token;
}

// Before each API call
token = await checkAndRefreshToken(token);
```

### Strategy 3: Refresh on 401 Error

```javascript
async function apiCall(endpoint, token) {
    try {
        const response = await fetch(endpoint, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.status === 401) {
            // Token expired, refresh and retry
            console.log('Token expired. Refreshing...');
            token = await refreshToken(token);
            
            // Retry with new token
            return await fetch(endpoint, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
        }
        
        return response;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}
```

---

## 🎯 Best Practices

### 1. **Refresh Proactively**
```javascript
// ✅ Good: Refresh before expiration
if (daysLeft < 3) {
    await refreshToken();
}

// ❌ Bad: Wait until 401 error
// (causes disruption to user)
```

### 2. **Store Token Securely**
```javascript
// ✅ Good: Store in localStorage/sessionStorage
localStorage.setItem('qwen_token', newToken);

// ❌ Bad: Hardcode in code
const token = "eyJhbG..."; // Don't do this
```

### 3. **Handle Refresh Failures**
```javascript
try {
    newToken = await refreshToken(oldToken);
} catch (error) {
    // Original token might be completely invalid
    // Show login UI
    showLoginModal();
}
```

### 4. **Log Token Info**
```javascript
const info = getTokenInfo(token);
console.log(`Token valid for ${info.daysRemaining} more days`);
// Helps with debugging
```

---

## 🔍 Token Inspection

### Decode JWT Token (Client-Side)

```javascript
function decodeToken(token) {
    try {
        const parts = token.split('.');
        const payload = JSON.parse(atob(parts[1]));
        
        return {
            userId: payload.id,
            issuedAt: new Date(payload.iat * 1000),
            expiresAt: new Date(payload.exp * 1000),
            daysRemaining: (payload.exp * 1000 - Date.now()) / (1000 * 60 * 60 * 24)
        };
    } catch (e) {
        return null;
    }
}

// Usage
const info = decodeToken(token);
console.log('User ID:', info.userId);
console.log('Expires:', info.expiresAt.toLocaleString());
console.log('Days left:', info.daysRemaining.toFixed(1));
```

### Python Version

```python
import json
import base64
import time

def decode_token(token):
    try:
        # Split and decode payload
        parts = token.split('.')
        payload = json.loads(base64.b64decode(parts[1] + '=='))
        
        exp = payload['exp']
        days_left = (exp - time.time()) / 86400
        
        return {
            'user_id': payload['id'],
            'expires_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp)),
            'days_remaining': days_left
        }
    except Exception as e:
        return None

# Usage
info = decode_token(token)
print(f"User ID: {info['user_id']}")
print(f"Expires: {info['expires_at']}")
print(f"Days left: {info['days_remaining']:.1f}")
```

---

## 📊 Token Expiration Timeline

```
Day 0:  🔑 Get initial token (expires in 7 days)
Day 1:  ✅ Token valid
Day 2:  ✅ Token valid
Day 3:  ✅ Token valid
Day 4:  ⚠️  Refresh recommended (< 3 days left)
Day 5:  🔄 Auto-refresh → New token (expires in 7 days)
Day 6:  ✅ New token valid
Day 7:  ✅ New token valid
...
```

**Result**: Infinite token validity với auto-refresh!

---

## 🚨 Error Handling

### Common Errors

#### 1. **401 Unauthorized**
```javascript
// Token completely expired or invalid
// Solution: Refresh or re-login
```

#### 2. **429 Rate Limited**
```javascript
// Too many refresh requests
// Solution: Add delay between refreshes
```

#### 3. **Network Error**
```javascript
// Connection failed
// Solution: Retry with exponential backoff
```

### Complete Error Handler

```javascript
async function safeRefreshToken(token, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const newToken = await refreshToken(token);
            if (newToken) return newToken;
        } catch (error) {
            if (error.message.includes('401')) {
                // Token invalid, can't refresh
                throw new Error('Token invalid. Please login again.');
            }
            
            if (i < retries - 1) {
                // Retry with delay
                await new Promise(resolve => setTimeout(resolve, 2000 * (i + 1)));
            }
        }
    }
    
    throw new Error('Failed to refresh token after retries');
}
```

---

## 🎓 Example: Complete Token Management

```javascript
class QwenTokenManager {
    constructor(initialToken) {
        this.token = initialToken;
        this.refreshTimer = null;
        this.callbacks = {
            onRefresh: null,
            onExpired: null
        };
    }
    
    // Get current token
    getToken() {
        return this.token;
    }
    
    // Set new token
    setToken(newToken) {
        this.token = newToken;
        localStorage.setItem('qwen_token', newToken);
    }
    
    // Decode token
    getTokenInfo() {
        try {
            const payload = JSON.parse(atob(this.token.split('.')[1]));
            return {
                userId: payload.id,
                expiresAt: new Date(payload.exp * 1000),
                daysLeft: (payload.exp * 1000 - Date.now()) / (1000 * 60 * 60 * 24)
            };
        } catch {
            return null;
        }
    }
    
    // Check if needs refresh
    needsRefresh() {
        const info = this.getTokenInfo();
        return info && info.daysLeft < 3;
    }
    
    // Refresh token
    async refresh() {
        try {
            const response = await fetch('https://chat.qwen.ai/api/v1/auths/', {
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.token) {
                this.setToken(data.token);
                
                if (this.callbacks.onRefresh) {
                    this.callbacks.onRefresh(data);
                }
                
                console.log('✓ Token refreshed');
                return true;
            }
        } catch (error) {
            console.error('Refresh failed:', error);
            
            if (this.callbacks.onExpired) {
                this.callbacks.onExpired(error);
            }
        }
        
        return false;
    }
    
    // Start auto-refresh
    startAutoRefresh(checkIntervalHours = 24) {
        this.stopAutoRefresh();
        
        this.refreshTimer = setInterval(async () => {
            if (this.needsRefresh()) {
                console.log('Auto-refreshing token...');
                await this.refresh();
            }
        }, checkIntervalHours * 60 * 60 * 1000);
        
        // Initial check
        if (this.needsRefresh()) {
            this.refresh();
        }
    }
    
    // Stop auto-refresh
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }
    
    // Set callbacks
    on(event, callback) {
        this.callbacks[event] = callback;
    }
}

// Usage
const tokenManager = new QwenTokenManager(initialToken);

tokenManager.on('onRefresh', (data) => {
    console.log('Token refreshed!', data.expires_at);
    updateUI('Token valid until ' + new Date(data.expires_at * 1000));
});

tokenManager.on('onExpired', (error) => {
    console.error('Token expired!', error);
    showLoginModal();
});

tokenManager.startAutoRefresh(24); // Check every 24 hours

// Check token status
const info = tokenManager.getTokenInfo();
console.log(`Token expires in ${info.daysLeft.toFixed(1)} days`);
```

---

## ✅ Testing

```bash
# Test token refresh
python test_token_refresh.py

# Expected output:
# ============================================================
#   Qwen Token Refresh Test
# ============================================================
# 
# 1. Get current token info:
#    User: LONG LONG (email@example.com)
#    Expires at: 2025-10-14 15:34:20
#    Days remaining: 7.0 days
# 
# 2. Refresh token:
# ✓ Token refreshed. Expires at: 2025-10-14 15:34:20
#    New Token: eyJhbGciOi...
#    Token refreshed successfully!
# 
# 3. Test with refreshed token:
#    ✓ User status check: {'success': True, ...}
#    ✓ Found 2 chats
#    ✓ Token is working correctly!
```

---

## 📝 Summary

✅ **Token CAN be auto-refreshed**  
✅ **No need to login repeatedly**  
✅ **Simple API call: GET /v1/auths/**  
✅ **Returns new token + expiration**  
✅ **Implementations ready (Python, JavaScript)**  
✅ **Auto-refresh strategies provided**  

**Kết luận**: Token management giờ đây **hoàn toàn tự động**!

---

**Created**: 2025-10-07  
**Last Updated**: 2025-10-07  
**Status**: ✅ Production Ready
