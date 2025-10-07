# Qwen API Research Documentation

## 🔍 Thông tin đã thu thập

### Authentication
- **Token Type**: JWT (JSON Web Token)
- **Token Location**: LocalStorage key `token`
- **Header Format**: `Authorization: Bearer <token>`
- **Token Example**:
  ```
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjA4NjV9.OGJIlTgWdKoQmSjULCrEPGFQ7xoCu5ao7fFoPO33pyE
  ```

### Base URL
```
https://chat.qwen.ai/api
```

### ✅ Hoạt động (Verified)

#### GET `/v2/users/status`
Kiểm tra trạng thái người dùng

**Response:**
```json
{
  "success": true,
  "request_id": "...",
  "data": true
}
```

#### GET `/v2/users/user/settings`
Lấy cài đặt người dùng

#### GET `/v2/chats?page=1`
Liệt kê các conversation

**Response:**
```json
{
  "success": true,
  "request_id": "...",
  "data": [
    {
      "id": "5182b415-9927-49f9-8d73-00d98fde8a0e",
      "title": "Friendly Greeting Chat",
      "updated_at": 1759815543,
      "created_at": 1759815505,
      "chat_type": "t2t"
    }
  ]
}
```

#### GET `/v2/chats/pinned`
Lấy các conversation đã pin

#### GET `/config`
Lấy cấu hình hệ thống

**Response:**
```json
{
  "status": true,
  "name": "Qwen",
  "version": "0.4.4",
  "features": {...}
}
```

### ❌ Không hoạt động

#### POST `/v2/chats` hoặc `/v2/chats/`
Tạo conversation mới - **Method Not Allowed**

#### POST `/v2/chats/{id}/messages`
Gửi tin nhắn - **Not Found** (có thể chat đã bị xóa)

#### POST `/chat/completions`
Chat completions API - **504 Gateway Timeout**

## 🎯 Hướng dẫn tìm API Endpoint chính xác

Qwen có thể sử dụng WebSocket hoặc Server-Sent Events (SSE) thay vì REST API thuần túy. Để tìm endpoint chính xác:

### Phương pháp 1: Browser Developer Tools

1. **Mở Qwen Chat**: https://chat.qwen.ai
2. **Mở Developer Tools** (F12)
3. **Chuyển sang tab Network**
4. **Filter**: Chọn `Fetch/XHR` hoặc `WS` (WebSocket)
5. **Gửi một tin nhắn** trong Qwen Chat
6. **Quan sát requests**:
   - Tìm request có path chứa `chat`, `message`, hoặc `completions`
   - Click vào request đó
   - Xem **Request URL**, **Method**, **Headers**, và **Payload**

### Phương pháp 2: Sử dụng HAR File

1. Trong Developer Tools > Network
2. Click biểu tượng **Export HAR**
3. Lưu file và tìm các requests liên quan đến chat

### Phương pháp 3: Sử dụng Browser Extension

Cài đặt extension như **Requestly** hoặc **ModHeader** để:
- Log tất cả requests
- Export requests dưới dạng curl commands

## 🔧 Các endpoint có thể thử thêm

Dựa trên các pattern phổ biến của chat applications:

```
# WebSocket
wss://chat.qwen.ai/ws
wss://chat.qwen.ai/api/v2/ws
wss://chat.qwen.ai/api/chat/ws

# Server-Sent Events
/api/v2/chats/{id}/stream
/api/v2/completions
/api/chat/stream

# Alternative REST endpoints
/api/v2/inference
/api/v2/generate
/api/assistant/chat
```

## 💡 Phát hiện quan trọng

1. **Qwen API sử dụng structure**: `{success: bool, request_id: string, data: any}`
2. **Token có expiration**: Token sẽ hết hạn sau một thời gian
3. **Rate limiting**: API có thể có giới hạn requests
4. **Geography-based routing**: Response headers có `GA-AP: ap-northeast-1`

## 📝 Những gì cần làm tiếp

1. **Monitor real browser requests** khi gửi tin nhắn thực sự
2. **Check WebSocket connections** - có thể Qwen dùng WS thay vì HTTP
3. **Reverse engineer JavaScript code** của Qwen web app
4. **Check for SSE (Server-Sent Events)** trong streaming responses

## 🚀 Sử dụng tạm thời

Trong khi chờ tìm ra API endpoint chính xác, bạn có thể:

1. **Sử dụng Selenium/Puppeteer** để tự động hóa browser
2. **Sử dụng official Qwen model** qua:
   - Alibaba Cloud (DashScope)
   - Hugging Face
   - Local deployment

## 📚 Resources

- Qwen Official: https://qwen.ai
- Qwen GitHub: https://github.com/QwenLM
- DashScope API: https://dashscope.aliyun.com
