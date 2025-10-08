# Security Configuration

## 🔒 Tính năng bảo mật

API đã được cấu hình với các tính năng bảo mật sau:

### 1. **Giới hạn môi trường**
- API chỉ hoạt động trong môi trường **development**
- Nếu `ENVIRONMENT=production`, tất cả API endpoints sẽ trả về lỗi 403

### 2. **Giới hạn domain (CORS)**
API chỉ chấp nhận requests từ các domain sau:
- `https://jlpt4you.com`
- `https://www.jlpt4you.com`
- `http://localhost:3000` (dev)
- `http://localhost:5000` (dev)
- `http://127.0.0.1:3000` (dev)
- `http://127.0.0.1:5000` (dev)

### 3. **Kiểm tra Origin và Referer**
- Kiểm tra `Origin` header từ browser
- Kiểm tra `Referer` header để đảm bảo request đến từ domain hợp lệ

## ⚙️ Cấu hình Vercel

### Environment Variables cần thiết:

```bash
# Required
QWEN_TOKEN=your_qwen_token_here
ADMIN_KEY=your_admin_key_here

# Security (Important!)
ENVIRONMENT=development  # Để API hoạt động
```

### Cách set environment variables trên Vercel:

1. Vào project dashboard: https://vercel.com/your-project
2. Settings → Environment Variables
3. Thêm các biến:
   - `QWEN_TOKEN`: Token từ Qwen
   - `ADMIN_KEY`: Key để quản lý API
   - `ENVIRONMENT`: Set là `development`

## 🧪 Testing

### Test từ jlpt4you.com:
```javascript
// Trong website jlpt4you.com
fetch('https://qwenai-two.vercel.app/api/chat/quick', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Xin chào!',
    model: 'qwen-plus'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Test local (development):
```bash
# Từ localhost sẽ hoạt động
curl -X POST http://localhost:5000/api/chat/quick \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"message": "Test", "model": "qwen-plus"}'
```

### Test từ domain khác (sẽ bị chặn):
```bash
# Sẽ trả về lỗi 403
curl -X POST https://qwenai-two.vercel.app/api/chat/quick \
  -H "Content-Type: application/json" \
  -H "Origin: https://example.com" \
  -d '{"message": "Test"}'
```

## 🚨 Lỗi thường gặp

### 1. "API is only available in development environment"
**Nguyên nhân**: `ENVIRONMENT` được set là `production`
**Giải pháp**: Set `ENVIRONMENT=development` trong Vercel env vars

### 2. "Access denied: Invalid origin"
**Nguyên nhân**: Request đến từ domain không được phép
**Giải pháp**: 
- Đảm bảo request từ `jlpt4you.com` hoặc `localhost`
- Kiểm tra CORS headers

### 3. "Access denied: Invalid referer"
**Nguyên nhân**: Referer header không hợp lệ
**Giải pháp**: Đảm bảo request được gửi từ browser trên domain hợp lệ

## 📝 Endpoints được bảo vệ

Tất cả các endpoint sau đều có security check:
- ✅ `/api/models`
- ✅ `/api/user/status`
- ✅ `/api/token/refresh`
- ✅ `/api/token/info`
- ✅ `/api/chats`
- ✅ `/api/chats/<chat_id>`
- ✅ `/api/chat/send`
- ✅ `/api/chat/quick`
- ✅ `/api/stats`

**Không** có security check:
- `/health` - Public health check endpoint
- `/api/admin/token` - Có bảo mật riêng bằng ADMIN_KEY

## 🔧 Tùy chỉnh

### Thêm domain mới:
Sửa file `api_server.py`:
```python
ALLOWED_ORIGINS = [
    'https://jlpt4you.com',
    'https://www.jlpt4you.com',
    'https://your-new-domain.com',  # Thêm domain mới
    # ...
]
```

### Tắt security (không khuyến khích):
Xóa decorator `@check_security()` khỏi các endpoints

### Chuyển sang production:
Set `ENVIRONMENT=production` để chặn tất cả requests
