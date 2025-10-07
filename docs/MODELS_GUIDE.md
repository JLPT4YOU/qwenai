# 🤖 Qwen Models - Complete Guide

## 📊 Available Models (19 models)

### 🏆 Flagship Models

#### 1. **Qwen3-Max** (Recommended)
- **Best for:** All-around tasks, most powerful
- **Context:** 256K tokens (262,144)
- **Max output:** 32K tokens
- **Capabilities:**
  - ✅ Vision (images, videos)
  - ✅ Document processing
  - ✅ Audio understanding
  - ✅ Citations (search with sources)
  - ✅ MCP (Model Context Protocol)
- **Supported modes:**
  - Text-to-text (t2t)
  - Text-to-video (t2v)
  - Text-to-image (t2i)
  - Image editing
  - 🌐 **Search**
  - Artifacts
  - Web development
  - Deep research
  - Travel planning
- **MCP Tools:**
  - Image generation
  - Code interpreter
  - AMap integration
  - Fire-crawl

#### 2. **Qwen3-VL-235B-A22B**
- **Best for:** Vision + Language tasks, multimodal
- **Context:** 256K tokens (up to 1M)
- **Capabilities:**
  - 💭 **Thinking** (with budget control)
  - ✅ Vision, Document, Video
  - ✅ Citations
  - OCR, spatial understanding, GUI tasks
- **Max thinking:** 81,920 tokens
- **Max summary:** 32,768 tokens

#### 3. **QVQ-Max**
- **Best for:** Vision + Reasoning
- **Specialized:** Vision Question Answering

---

### 💻 Coding Models

#### 4. **Qwen3-Coder**
- **Best for:** Code generation & debugging
- **Optimized for:** Programming tasks

#### 5. **Qwen3-Coder-Flash**
- **Best for:** Fast code completion
- **Optimized for:** Speed

#### 6. **Qwen2.5-Coder-32B-Instruct**
- **Best for:** Instruct-based coding
- **Size:** 32B parameters

---

### ⚡ Fast Models

#### 7. **Qwen3-Omni-Flash**
- **Best for:** Quick multimodal responses
- **Optimized for:** Speed + multimodal

#### 8. **Qwen2.5-Turbo**
- **Best for:** Fast text generation
- **Optimized for:** Speed

---

### 🧠 Reasoning Models

#### 9. **QwQ-32B**
- **Best for:** Complex reasoning
- **Specialized:** Question answering with reasoning

---

### 🎯 Specialized Models

#### 10. **Qwen3-Next-80B-A3B**
- Next-generation model (80B)

#### 11. **Qwen3-235B-A22B-2507**
- Large-scale model (235B)

#### 12. **Qwen3-30B-A3B-2507**
- Mid-size model (30B)

#### 13. **Qwen3-VL-30B-A3B**
- Vision-Language (30B)

#### 14. **Qwen2.5-Max**
- Previous generation flagship

#### 15. **Qwen2.5-Plus**
- Enhanced 2.5 version

#### 16. **Qwen2.5-Omni-7B**
- Small multimodal (7B)

#### 17. **Qwen2.5-VL-32B-Instruct**
- Vision-Language instruct

#### 18. **Qwen2.5-14B-Instruct-1M**
- 1M context window!

#### 19. **Qwen2.5-72B-Instruct**
- Large instruct model (72B)

---

## 🎯 Model Selection Guide

### By Use Case

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| **General Chat** | Qwen3-Max | Most powerful, all features |
| **Coding** | Qwen3-Coder | Optimized for code |
| **Fast Response** | Qwen3-Omni-Flash | Speed |
| **Vision Tasks** | Qwen3-VL-235B-A22B | Best vision model |
| **Reasoning** | QwQ-32B | Specialized reasoning |
| **Long Context** | Qwen2.5-14B-Instruct-1M | 1M context! |
| **Search + Chat** | Qwen3-Max | Built-in search |
| **Thinking Mode** | Qwen3-VL-235B-A22B | Thinking capability |

---

## 💻 Usage

### Python Client

```python
from qwen_client import QwenClient

client = QwenClient(token)

# List available models
models = client.list_models()

for model in models['data']:
    name = model['name']
    caps = model['info']['meta']['capabilities']
    print(f"{name}: {caps}")

# Use specific model
response = client.send_message(
    chat_id=chat_id,
    message="Write Python code",
    model="qwen3-coder"  # Use coding model
)

# Use with thinking
response = client.send_message(
    chat_id=chat_id,
    message="Complex problem",
    model="qwen3-vl-plus",  # Qwen3-VL-235B-A22B
    thinking_enabled=True
)
```

### API Direct

```bash
# List models
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5001/api/models

# Use specific model
curl -X POST http://localhost:5001/api/chat/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "chat-id",
    "message": "Hello",
    "model": "qwen3-coder"
  }'
```

---

## 🔧 Model Capabilities

### Context Length

| Model | Context | Notes |
|-------|---------|-------|
| Qwen3-Max | 256K | Standard |
| Qwen2.5-14B-Instruct-1M | **1M** | Longest! |
| Qwen3-VL-235B-A22B | 256K-1M | Variable |

### Special Features

#### 💭 Thinking Mode
- **Models:** Qwen3-VL-235B-A22B
- **Max thinking tokens:** 81,920
- **Use for:** Complex reasoning, math, logic

#### 🌐 Search/Citations
- **Models:** Qwen3-Max, Qwen3-VL-235B-A22B
- **Feature:** Internet search with source citations
- **Format:** [[1]][[2]][[3]] references

#### 👁️ Vision
- **Models:** Qwen3-Max, Qwen3-VL-*
- **Supports:** Images, videos, documents, OCR

#### 🔊 Audio
- **Models:** Qwen3-Max
- **Feature:** Audio understanding

#### 🎨 Image Generation
- **Models:** Qwen3-Max (via MCP)
- **Types:** Text-to-image, image editing

---

## 📝 Model IDs Reference

For use in API calls:

```python
MODELS = {
    "qwen3-max": "Qwen3-Max",
    "qwen3-vl-plus": "Qwen3-VL-235B-A22B",
    "qwen3-coder": "Qwen3-Coder",
    "qwen3-vl": "Qwen3-VL-30B-A3B",
    "qwen3-omni-flash": "Qwen3-Omni-Flash",
    "qwen3-next": "Qwen3-Next-80B-A3B",
    "qwen3-235b": "Qwen3-235B-A22B-2507",
    "qwen3-30b": "Qwen3-30B-A3B-2507",
    "qwen3-coder-flash": "Qwen3-Coder-Flash",
    "qwen2.5-max": "Qwen2.5-Max",
    "qwen2.5-plus": "Qwen2.5-Plus",
    "qwq-32b": "QwQ-32B",
    "qwen2.5-turbo": "Qwen2.5-Turbo",
    "qwen2.5-omni-7b": "Qwen2.5-Omni-7B",
    "qvq-max": "QVQ-Max",
    "qwen2.5-vl-32b-instruct": "Qwen2.5-VL-32B-Instruct",
    "qwen2.5-14b-instruct-1m": "Qwen2.5-14B-Instruct-1M",
    "qwen2.5-coder-32b-instruct": "Qwen2.5-Coder-32B-Instruct",
    "qwen2.5-72b-instruct": "Qwen2.5-72B-Instruct"
}
```

---

## 🎯 Quick Recommendations

### For Beginners
```python
model = "qwen3-max"  # Best all-around
```

### For Developers
```python
model = "qwen3-coder"  # Code-specific
```

### For Speed
```python
model = "qwen3-omni-flash"  # Fastest
```

### For Reasoning
```python
model = "qwen3-vl-plus"  # With thinking
thinking_enabled = True
```

### For Research
```python
model = "qwen3-max"  # With search
search_enabled = True
```

### For Long Documents
```python
model = "qwen2.5-14b-instruct-1m"  # 1M context!
```

---

## 📊 Performance Comparison

| Model | Speed | Quality | Cost | Context |
|-------|-------|---------|------|---------|
| Qwen3-Max | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 256K |
| Qwen3-Coder | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 | - |
| Qwen3-Omni-Flash | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰 | - |
| Qwen3-VL-235B | ⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰 | 256K-1M |
| Qwen2.5-Turbo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 💰 | - |

---

## 🔄 Model Updates

Models are continuously updated. Check for latest:

```python
models = client.list_models()
latest = [m for m in models['data'] if '3' in m['name']]
print("Latest models:", [m['name'] for m in latest])
```

---

## 📖 Documentation

See full model details in `models_response.json`.

**Key fields:**
- `id`: Model ID for API calls
- `name`: Display name
- `meta.capabilities`: Feature flags
- `meta.max_context_length`: Token limit
- `meta.chat_type`: Supported modes
- `meta.mcp`: Available tools

---

## 🎉 Summary

✅ **19 models available**  
✅ **Flagship: Qwen3-Max** (all features)  
✅ **Coding: Qwen3-Coder** (optimized)  
✅ **Vision: Qwen3-VL-235B-A22B** (with thinking)  
✅ **Long context: Qwen2.5-14B-Instruct-1M** (1M tokens!)  
✅ **Features: Search, Thinking, Vision, Audio**

**Default recommendation: `qwen3-max`** 🏆

---

**Last updated:** 2025-10-07  
**API version:** v2  
**Total models:** 19
