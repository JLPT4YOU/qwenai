# 🚀 Quick Start Guide - Qwen AI Chat

## 📌 Tóm tắt

Dự án này cung cấp 2 cách để sử dụng Qwen AI:

1. **✅ Official API (Khuyến nghị)** - Sử dụng DashScope API chính thức
2. **⚠️ Web API (Thực nghiệm)** - Reverse engineer từ Qwen web chat

---

## Phương pháp 1: Official API (Khuyến nghị) ✅

### Ưu điểm
- ✅ Chính thức và được support
- ✅ Ổn định và đáng tin cậy  
- ✅ Documentation đầy đủ
- ✅ Có free tier để test

### Cài đặt

```bash
# 1. Cài dependencies
pip install requests

# 2. Lấy API key
# Truy cập: https://dashscope.console.aliyun.com/
# Đăng ký / Đăng nhập -> API Keys -> Tạo key mới

# 3. Set environment variable
export DASHSCOPE_API_KEY='your_api_key_here'

# 4. Test
python qwen_official_client.py "Hello, introduce yourself"
```

### Sử dụng trong code

```python
from qwen_official_client import QwenOfficialClient

# Khởi tạo
client = QwenOfficialClient(api_key="your_api_key")

# Chat đơn giản
response = client.chat("What is Python?")
print(response)

# Chat với context
history = [
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "Hello Alice! Nice to meet you."}
]
response = client.chat("What's my name?", history=history)
print(response)

# Tùy chỉnh parameters
response = client.chat(
    message="Write a poem",
    model="qwen-max",
    temperature=0.9,
    max_tokens=1000
)
```

### Available Models

- `qwen-max` - Mạnh nhất, chất lượng cao nhất
- `qwen-plus` - Cân bằng giữa performance và cost
- `qwen-turbo` - Nhanh và rẻ nhất
- `qwen-vl-max` - Multimodal (text + image)

---

## Phương pháp 2: Web API (Thực nghiệm) ⚠️

### Cảnh báo
- ⚠️ Unofficial API - có thể thay đổi bất cứ lúc nào
- ⚠️ Chưa tìm ra endpoint gửi message chính xác
- ⚠️ Token có thời hạn và cần refresh thường xuyên

### Cài đặt

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Lấy token từ browser
# Truy cập: https://chat.qwen.ai
# Đăng nhập -> F12 -> Application -> Local Storage -> Copy 'token'

# 3. Set token
export QWEN_TOKEN='your_jwt_token_here'
```

### Status hiện tại

Đã tìm ra:
- ✅ Authentication mechanism (JWT token)
- ✅ GET endpoints (list chats, user info, etc.)
- ❌ POST endpoints (create chat, send message) - **Chưa hoạt động**

Xem `API_RESEARCH.md` để biết chi tiết và cách tìm endpoint chính xác.

---

## 📊 So sánh

| Feature | Official API | Web API |
|---------|-------------|---------|
| **Độ ổn định** | Cao ✅ | Thấp ⚠️ |
| **Documentation** | Có ✅ | Không ❌ |
| **Setup** | Dễ | Phức tạp |
| **Cost** | Pay as you go | Free (dùng web account) |
| **API calls** | Unlimited | Có rate limit |
| **Models** | Tất cả | Chỉ models trên web |

---

## 🎯 Khuyến nghị

### Dùng Official API nếu:
- Bạn cần API ổn định cho production
- Bạn không ngại trả phí (có free tier)
- Bạn cần documentation và support

### Dùng Web API nếu:
- Bạn chỉ cần test/experiment
- Bạn sẵn sàng tự reverse engineer
- Bạn có sẵn Qwen web account

---

## 📚 Next Steps

1. **Nếu dùng Official API**: Xem `qwen_official_client.py` và test ngay
2. **Nếu dùng Web API**: Đọc `API_RESEARCH.md` để tìm endpoints
3. **Cần interactive chatbot**: Chờ hoàn thành API research

---

## 🆘 Troubleshooting

### Official API: "Invalid API key"
- Kiểm tra API key có đúng không
- Kiểm tra account còn credits không
- Đảm bảo đã export DASHSCOPE_API_KEY

### Web API: "Failed to create chat"
- Token có thể đã hết hạn - lấy token mới
- Endpoint chưa được tìm ra - xem API_RESEARCH.md
- Thử monitor browser requests để tìm endpoint đúng

---

## 📞 Support

- **Official API Docs**: https://help.aliyun.com/zh/dashscope/
- **Qwen GitHub**: https://github.com/QwenLM
- **Issues**: Tạo issue trong repository này
