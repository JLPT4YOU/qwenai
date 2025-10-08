# 🤖 Qwen Models - Quick Reference

## 🎯 Most Common Models

### **qwen3-max** (Default - Recommended)
- ✅ **Best all-around model**
- ✅ Vision (images, videos)
- ✅ Document processing
- ✅ 256K context
- ✅ Search capability
- **Use for:** General chat, file upload, most tasks

### **qwen-plus**
- ⚡ **Faster, cheaper**
- ✅ Good for simple tasks
- ✅ 128K context
- **Use for:** Quick responses, simple questions

### **qwen-turbo**
- ⚡⚡ **Fastest, cheapest**
- ✅ Basic tasks only
- ✅ 8K context
- **Use for:** Very simple queries

---

## 🖼️ Vision Models (for images)

### **qwen-vl-max**
- 🎨 **Best for vision tasks**
- ✅ OCR, image analysis
- ✅ 32K context
- **Use for:** Image understanding, OCR

### **qwen-vl-plus**
- 🎨 **Faster vision**
- ✅ Good for simple image tasks
- **Use for:** Quick image analysis

### **qwen3-vl-235b-a22b**
- 💭 **Vision + Thinking**
- ✅ Deep reasoning about images
- ✅ 256K context
- **Use for:** Complex visual reasoning

---

## 💻 Coding Models

### **qwen-coder-plus**
- 💻 **Best for coding**
- ✅ Code generation
- ✅ 128K context
- **Use for:** Programming tasks

### **qwen-coder-turbo**
- 💻⚡ **Fast coding**
- ✅ Quick code snippets
- **Use for:** Simple code generation

---

## 🧮 Math Models

### **qwen-math-plus**
- 🧮 **Math specialist**
- ✅ Complex calculations
- ✅ Math reasoning
- **Use for:** Math problems, equations

### **qwen-math-turbo**
- 🧮⚡ **Fast math**
- **Use for:** Simple calculations

---

## 💭 Thinking Models

### **qwq-32b-preview**
- 💭 **Deep reasoning**
- ✅ Step-by-step thinking
- ✅ 32K context
- **Use for:** Complex problem solving

---

## 📝 Usage Examples

### Python Client

```python
from qwen_client import QwenClient

client = QwenClient(auth_token=token)

# Default model (qwen3-max)
response = client.chat("Hello")

# Specify different model
response = client.chat("Hello", model="qwen-plus")

# Vision model for images
response = client.chat_with_files(
    message="What's in this image?",
    files=["image.jpg"],
    model="qwen-vl-max"  # Best for vision
)

# Coding model
response = client.chat(
    "Write a Python function",
    model="qwen-coder-plus"
)

# Math model
response = client.chat(
    "Solve: x^2 + 5x + 6 = 0",
    model="qwen-math-plus"
)

# Thinking model
response = client.send_message(
    chat_id=chat_id,
    message="Complex reasoning task",
    model="qwq-32b-preview",
    thinking_enabled=True
)
```

### REST API

```bash
# Default model
curl -X POST http://localhost:5001/api/chat/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-id",
    "message": "Hello"
  }'

# Specify model
curl -X POST http://localhost:5001/api/chat/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-id",
    "message": "Hello",
    "model": "qwen-plus"
  }'

# Vision model with file
curl -X POST http://localhost:5001/api/chat/send-with-files \
  -H "Authorization: Bearer $TOKEN" \
  -F "message=Analyze this image" \
  -F "files=@image.jpg" \
  -F "model=qwen-vl-max"
```

### JavaScript

```javascript
// Default model
const response = await fetch('/api/chat/send', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        chat_id: chatId,
        message: 'Hello'
    })
});

// Specify model
const response = await fetch('/api/chat/send', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        chat_id: chatId,
        message: 'Hello',
        model: 'qwen-plus'  // Override default
    })
});
```

---

## 🎯 Model Selection Guide

### For File Upload (Images + Documents)

```python
# Images - Use vision models
client.chat_with_files(
    message="Describe this image",
    files=["photo.jpg"],
    model="qwen-vl-max"  # Best for images
)

# Documents - Use general models
client.chat_with_files(
    message="Summarize this PDF",
    files=["document.pdf"],
    model="qwen3-max"  # Best for documents
)

# Mixed (images + documents)
client.chat_with_files(
    message="Analyze these files",
    files=["image.jpg", "doc.pdf"],
    model="qwen3-max"  # Handles both
)
```

### For Different Tasks

| Task | Recommended Model | Alternative |
|------|-------------------|-------------|
| **General chat** | `qwen3-max` | `qwen-plus` |
| **Image analysis** | `qwen-vl-max` | `qwen3-max` |
| **OCR** | `qwen-vl-max` | `qwen-vl-plus` |
| **Document Q&A** | `qwen3-max` | `qwen-plus` |
| **Coding** | `qwen-coder-plus` | `qwen-coder-turbo` |
| **Math** | `qwen-math-plus` | `qwen-math-turbo` |
| **Complex reasoning** | `qwq-32b-preview` | `qwen3-max` |
| **Fast responses** | `qwen-turbo` | `qwen-plus` |
| **Search** | `qwen3-max` | - |

---

## ⚙️ Default Model Configuration

All methods use `qwen3-max` as default but can be overridden:

```python
# qwen_client.py
def chat(self, message: str, model: str = "qwen3-max", ...):
def send_message(self, chat_id: str, message, model: str = "qwen3-max", ...):
def chat_with_files(self, message: str, files, model: str = "qwen3-max", ...):
def create_chat(self, title: str = "New Chat", model: str = "qwen3-max", ...):
```

**To change default globally**, edit `qwen_client.py` or always pass `model` parameter.

---

## 💡 Tips

1. **For file upload**: Use `qwen3-max` (handles both images and documents)
2. **For pure vision**: Use `qwen-vl-max` (better OCR, image understanding)
3. **For speed**: Use `qwen-plus` or `qwen-turbo`
4. **For coding**: Use `qwen-coder-plus`
5. **For math**: Use `qwen-math-plus`
6. **For deep thinking**: Use `qwq-32b-preview` with `thinking_enabled=True`

---

## 📚 Full Model List

See `/docs/MODELS_GUIDE.md` for complete details on all 19 models.

---

## 🔗 Related Documentation

- **Full Models Guide**: `/docs/MODELS_GUIDE.md`
- **File Upload**: `/docs/FILE_UPLOAD_API.md`
- **API Reference**: `/API_DOCS.md`
