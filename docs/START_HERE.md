# 🚀 Bắt Đầu Ngay - Qwen AI Chatbot

## ⚡ Quick Start (5 phút)

### Option 1: Web API (Miễn phí - Khuyến nghị cho testing)

```bash
# Bước 1: Lấy token
# 1. Truy cập: https://chat.qwen.ai
# 2. Đăng nhập
# 3. Nhấn F12 > Application > Local Storage
# 4. Copy giá trị của key "token"

# Bước 2: Set token
export QWEN_TOKEN='paste_your_token_here'

# Bước 3: Test ngay!
python qwen_client.py "Hello! Tell me a joke"
```

### Option 2: Official API (Production-ready)

```bash
# Bước 1: Lấy API key
# Truy cập: https://dashscope.console.aliyun.com/
# Tạo API key mới

# Bước 2: Set key
export DASHSCOPE_API_KEY='your_api_key'

# Bước 3: Test
python qwen_official_client.py "What is AI?"
```

## 📁 Files quan trọng

| File | Mô tả |
|------|-------|
| `qwen_client.py` | ⭐ Web API client - Dùng ngay |
| `qwen_official_client.py` | Official API client |
| `chatbot.py` | Interactive chatbot |
| `README.md` | 📖 Documentation đầy đủ |
| `QUICK_START.md` | Hướng dẫn chi tiết |
| `SUCCESS_SUMMARY.md` | ✅ Tổng kết project |

## 🎯 Commands hữu ích

```bash
# List chats của bạn
python qwen_client.py --list-chats

# Gửi message
python qwen_client.py "Your question here"

# Interactive chatbot
python chatbot.py

# Examples
python example.py
```

## 💡 Tips

1. **Token hết hạn?** Lấy token mới từ browser (F12 > Local Storage)
2. **Muốn stable API?** Dùng Official API với DashScope
3. **Debug?** Xem `API_RESEARCH.md` để hiểu cách API hoạt động
4. **Customize?** Code đã documented đầy đủ, dễ modify

## 🆘 Troubleshooting

**Lỗi: "QWEN_TOKEN not set"**
```bash
export QWEN_TOKEN='your_token_from_browser'
```

**Lỗi: "No existing chats found"**
- Vào https://chat.qwen.ai tạo một chat mới
- Hoặc dùng Official API

**Lỗi: "Model not found"**
- Model name đúng là `qwen3-max` (không phải `qwen-max`)

## 📚 Đọc thêm

- **Full docs**: `README.md`
- **Quick start**: `QUICK_START.md`
- **API research**: `API_RESEARCH.md`
- **Examples**: `example.py`

## ✨ Tính năng

- ✅ Chat với Qwen AI
- ✅ Streaming responses (real-time)
- ✅ List và quản lý conversations
- ✅ Interactive chatbot
- ✅ Cả Web API và Official API
- ✅ Documentation đầy đủ

## 🎊 Kết quả

**Working example:**
```
$ python qwen_client.py "What is 2+2?"

You: What is 2+2?
AI: The answer is 4. 

2 + 2 equals 4.
```

---

**Status**: ✅ Sẵn sàng sử dụng  
**Last Updated**: 2025-10-07  
**Version**: 1.0.0
