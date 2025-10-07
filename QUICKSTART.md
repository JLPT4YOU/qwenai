# ⚡ Quick Start - 5 Minutes to Deploy

## 🎯 Mục Tiêu

Tạo API Qwen cá nhân trên Vercel để dùng riêng.

---

## 🚀 Bước 1: Lấy Token (1 phút)

1. Vào https://chat.qwen.ai
2. Nhấn `F12` → **Application** → **Cookies**
3. Copy giá trị của `token`

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📦 Bước 2: Push Lên GitHub (2 phút)

```bash
# Khởi tạo repo
git init
git add .
git commit -m "Initial commit"

# Tạo repo trên GitHub, sau đó:
git remote add origin https://github.com/your-username/qwen-api.git
git push -u origin main
```

---

## ☁️ Bước 3: Deploy Lên Vercel (2 phút)

### Option A: Web Interface

1. Vào https://vercel.com/new
2. **Import** repo từ GitHub
3. **Add Environment Variables:**
   ```
   QWEN_TOKEN = your_token_here
   ADMIN_KEY = random_secure_string
   ```
   (Generate ADMIN_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
4. Click **Deploy**

### Option B: CLI

```bash
# Cài Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add env vars
vercel env add QWEN_TOKEN production
vercel env add ADMIN_KEY production

# Deploy production
vercel --prod
```

---

## ✅ Bước 4: Test API (30 giây)

```bash
# Test
curl -X POST https://your-project.vercel.app/api/chat/quick \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Hello!"}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "content": "Hello! How can I help you?"
  }
}
```

**🎉 DONE!** API của bạn đã sẵn sàng!

---

## 💡 Cách Dùng

### Python
```python
import requests

API = "https://your-project.vercel.app"
TOKEN = "your-token"

def ask(question):
    r = requests.post(
        f"{API}/api/chat/quick",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"message": question}
    )
    return r.json()["data"]["content"]

print(ask("What is Python?"))
```

### cURL
```bash
curl -X POST https://your-project.vercel.app/api/chat/quick \
  -H "Authorization: Bearer TOKEN" \
  -d '{"message": "Your question"}'
```

### JavaScript
```javascript
const API = "https://your-project.vercel.app";
const TOKEN = "your-token";

async function ask(message) {
  const response = await fetch(`${API}/api/chat/quick`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message })
  });
  const data = await response.json();
  return data.data.content;
}

ask("Hello!").then(console.log);
```

---

## 🎨 Features

### Chọn Model
```bash
curl -X POST $API/api/chat/quick \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Write Python code",
    "model": "qwen3-coder"
  }'
```

**Models:**
- `qwen3-max` - Tốt nhất (mặc định)
- `qwen3-coder` - Lập trình
- `qwen3-omni-flash` - Nhanh
- `qwq-32b` - Reasoning

### Thinking Mode (Hiện Suy Nghĩ)
```bash
curl -X POST $API/api/chat/quick \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Giải toán: 5 người bắt tay, mỗi người bắt tay 1 lần với mọi người khác",
    "thinking_enabled": true
  }'
```

### Internet Search
```bash
curl -X POST $API/api/chat/quick \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Tin tức AI hôm nay",
    "search_enabled": true
  }'
```

### System Prompt (Hướng Dẫn AI)
```bash
curl -X POST $API/api/chat/quick \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Giải thích Python",
    "system_prompt": "Trả lời ngắn gọn, tối đa 2 câu"
  }'
```

### Tất Cả Cùng Lúc
```bash
curl -X POST $API/api/chat/quick \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Phân tích xu hướng Python 2025",
    "model": "qwen3-max",
    "thinking_enabled": true,
    "search_enabled": true,
    "system_prompt": "Bạn là Python expert"
  }'
```

---

## 🔄 Khi Token Hết Hạn (Sau 7 Ngày)

### Cách 1: API Update (5 giây, không cần redeploy!)
```bash
# Lấy token mới từ browser
# chat.qwen.ai → F12 → Cookies → token

# Update via API
curl -X POST https://your-project.vercel.app/api/admin/token \
  -d '{
    "token": "NEW_TOKEN",
    "admin_key": "YOUR_ADMIN_KEY"
  }'
```

### Cách 2: Vercel Dashboard (30 giây)
1. Vercel → Project → Settings → Environment Variables
2. Edit `QWEN_TOKEN` → Paste token mới
3. Redeploy

---

## 📚 Tài Liệu

- **[API_DOCS.md](./API_DOCS.md)** - API reference đầy đủ
- **[DEPLOY.md](./DEPLOY.md)** - Hướng dẫn deploy chi tiết
- **[README.md](./README.md)** - Overview dự án

---

## ❓ Câu Hỏi Thường Gặp

**Q: Token hết hạn sau bao lâu?**  
A: Khoảng 7 ngày. Update qua API không cần redeploy.

**Q: API có giới hạn requests không?**  
A: Không! Dùng tài khoản Qwen của bạn nên không giới hạn.

**Q: Chi phí?**  
A: $0 - Vercel free tier đủ dùng.

**Q: Có thể dùng custom domain không?**  
A: Có! Vercel → Settings → Domains → Add domain.

**Q: Có thể thay đổi model không?**  
A: Có! 19 models khả dụng. Xem [MODELS_GUIDE.md](./docs/MODELS_GUIDE.md)

---

## 🎯 Next Steps

1. ✅ Deploy xong
2. 📖 Đọc [API_DOCS.md](./API_DOCS.md)
3. 🧪 Test các features
4. 🚀 Integrate vào app của bạn!

---

**Tổng thời gian:** 5 phút  
**Chi phí:** $0  
**Khó:** ⭐ (Rất dễ)

🎉 **Chúc bạn thành công!**
