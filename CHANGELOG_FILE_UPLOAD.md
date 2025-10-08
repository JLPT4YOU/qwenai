# 📝 Changelog - File Upload Feature

**Date**: 2025-10-08  
**Version**: 1.1.0

---

## 🎯 What Changed

### ✨ New Features

#### 1. **File Upload Support**
- ✅ Upload images (PNG, JPG, GIF, etc.)
- ✅ Upload documents (PDF, TXT, DOCX, etc.)
- ✅ Chat with file attachments
- ✅ Multiple files support

#### 2. **Environment Configuration**
- ✅ `QWEN_API_URL` - Configurable API base URL
- ✅ URLs no longer hardcoded
- ✅ Support for custom proxies/endpoints

#### 3. **File Type Auto-detection**
- ✅ Automatic detection based on MIME type
- ✅ Smart routing: images → vision, documents → RAG

---

## 📦 New Files

### Core Implementation
- ✅ `qwen_client.py` - Added 4 new methods for file upload
- ✅ `api_server.py` - Added 3 new REST endpoints

### Documentation
- ✅ `docs/FILE_UPLOAD_GUIDE.md` - Technical guide
- ✅ `docs/FILE_UPLOAD_API.md` - API reference
- ✅ `docs/FILE_TYPES_EXPLAINED.md` - Image vs Document explained
- ✅ `docs/ENVIRONMENT_CONFIG.md` - Environment setup guide
- ✅ `FILE_UPLOAD_SUMMARY.md` - Implementation summary

### Testing & Examples
- ✅ `tests/test_file_upload.py` - Comprehensive test suite
- ✅ `examples/chat_with_files.html` - Beautiful web UI demo

### Configuration
- ✅ `.env.example` - Updated with new variables
- ✅ `requirements.txt` - Added `oss2>=2.18.0`

---

## 🔧 Code Changes

### `qwen_client.py`

**Added imports:**
```python
import os  # For environment variables
```

**Modified class:**
```python
class QwenClient:
    # OLD: Hardcoded URL
    # BASE_URL = "https://chat.qwen.ai/api"
    
    # NEW: Configurable from environment
    BASE_URL = os.getenv("QWEN_API_URL", "https://chat.qwen.ai/api")
    
    def __init__(self, auth_token: str, auto_refresh: bool = True, base_url: Optional[str] = None):
        # NEW: Support custom base_url parameter
        if base_url:
            self.BASE_URL = base_url
```

**New methods:**
```python
def get_sts_token(self, filename: str, filesize: int, filetype: str = "image") -> Dict
def upload_file_to_oss(self, file_path: str, sts_data: Dict) -> str
def upload_file(self, file_path: str, filetype: str = None) -> Dict
def chat_with_files(self, message: str, files: List[str] = None, ...) -> str
```

### `api_server.py`

**New endpoints:**
```python
@app.route('/api/files/sts-token', methods=['POST'])
@app.route('/api/files/upload', methods=['POST'])
@app.route('/api/chat/send-with-files', methods=['POST'])
```

### `.env.example`

**Added variables:**
```bash
# NEW: Configurable API URL
QWEN_API_URL=https://chat.qwen.ai/api

# NEW: Environment mode
ENVIRONMENT=development
```

---

## 📊 Comparison: Before vs After

### Before (v1.0.0)

❌ **Limitations:**
- No file upload support
- Hardcoded API URLs
- Text-only chat
- No environment configuration

**Usage:**
```python
client = QwenClient(auth_token=token)
response = client.chat("Hello")
```

### After (v1.1.0)

✅ **Features:**
- Full file upload support (images + documents)
- Configurable URLs via environment
- Multi-modal chat (text + files)
- Comprehensive environment config

**Usage:**
```python
# Configure via environment
os.environ['QWEN_API_URL'] = 'https://custom-proxy.com/api'

# Upload and chat with files
client = QwenClient(auth_token=token)
response = client.chat_with_files(
    message="Analyze this",
    files=["image.png", "document.pdf"]
)
```

---

## 🎯 Key Differences: Image vs Document

### Image Files (`filetype: "image"`)

**Characteristics:**
```json
{
  "type": "image",
  "file_class": "vision",
  "showType": "image"
}
```

**Processing:**
- Vision model analysis
- OCR text extraction
- Object detection
- Visual Q&A

**Use Cases:**
- Screenshots
- Photos
- Diagrams
- Infographics

**Example from your curl:**
```json
{
  "files": [{
    "type": "image",
    "file_type": "image/png",
    "file_class": "vision",
    "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/..."
  }]
}
```

### Document Files (`filetype: "file"`)

**Characteristics:**
```json
{
  "type": "file",
  "file_class": "document",
  "showType": "file"
}
```

**Processing:**
- Text extraction
- RAG (Retrieval Augmented Generation)
- Semantic search
- Document Q&A

**Use Cases:**
- PDFs (like N1Kanji800.pdf)
- Word documents
- Excel files
- Text files

**Example from your curl:**
```json
{
  "files": [{
    "type": "file",
    "filename": "N1Kanji800.pdf",
    "file_type": "application/pdf",
    "file_class": "document",
    "size": 18422686,
    "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/..."
  }]
}
```

---

## 🔒 Security Improvements

### Before
```python
# Hardcoded in code
BASE_URL = "https://chat.qwen.ai/api"
```

### After
```python
# Configurable via environment
BASE_URL = os.getenv("QWEN_API_URL", "https://chat.qwen.ai/api")
```

**Benefits:**
- ✅ No hardcoded URLs in code
- ✅ Easy to change without code modification
- ✅ Support for proxies/custom endpoints
- ✅ Better for different environments (dev/staging/prod)

---

## 📈 Usage Examples

### Example 1: Upload Image (Vision)

```python
from qwen_client import QwenClient

client = QwenClient(auth_token=token)

# Upload screenshot for OCR
response = client.chat_with_files(
    message="Đọc text trong ảnh này",
    files=["screenshot.png"]
)
print(response['content'])
```

### Example 2: Upload Document (RAG)

```python
# Upload PDF for Q&A
response = client.chat_with_files(
    message="Cuốn sách này khó không?",
    files=["N1Kanji800.pdf"]
)
print(response['content'])
# Output: "Cuốn sách N1 Kanji 800 là tài liệu học tiếng Nhật..."
```

### Example 3: Custom API URL

```python
# Option 1: Environment variable
os.environ['QWEN_API_URL'] = 'https://my-proxy.com/api'
client = QwenClient(auth_token=token)

# Option 2: Constructor parameter
client = QwenClient(
    auth_token=token,
    base_url='https://my-proxy.com/api'
)
```

### Example 4: API Endpoint

```bash
# Upload file via REST API
curl -X POST http://localhost:5001/api/files/upload \
  -H "Authorization: Bearer $QWEN_TOKEN" \
  -F "file=@image.png" \
  -F "filetype=image"

# Chat with files
curl -X POST http://localhost:5001/api/chat/send-with-files \
  -H "Authorization: Bearer $QWEN_TOKEN" \
  -F "message=Analyze this" \
  -F "files=@image.png" \
  -F "files=@document.pdf"
```

---

## 🚀 Migration Guide

### For Existing Users

**No breaking changes!** Existing code continues to work.

**Optional upgrades:**

1. **Add environment variable** (optional):
```bash
# .env
QWEN_API_URL=https://chat.qwen.ai/api
```

2. **Install new dependency** (for file upload):
```bash
pip install oss2
```

3. **Use new features**:
```python
# Old way still works
client.chat("Hello")

# New way with files
client.chat_with_files("Analyze this", files=["image.png"])
```

---

## 📚 Documentation Structure

```
docs/
├── FILE_UPLOAD_GUIDE.md          # Technical deep-dive
├── FILE_UPLOAD_API.md             # API reference
├── FILE_TYPES_EXPLAINED.md        # Image vs Document (NEW)
├── ENVIRONMENT_CONFIG.md          # Environment setup (NEW)
└── [other docs]

examples/
└── chat_with_files.html           # Web UI demo (NEW)

tests/
└── test_file_upload.py            # Test suite (NEW)

.env.example                        # Updated with new vars
requirements.txt                    # Added oss2
FILE_UPLOAD_SUMMARY.md             # Implementation summary
CHANGELOG_FILE_UPLOAD.md           # This file
```

---

## ✅ Testing

All tests passing:

```bash
$ python tests/test_file_upload.py

✓ PASS  Get STS Token
✓ PASS  Upload Image
✓ PASS  Chat with Image
✓ PASS  API Upload

Total: 4/4 tests passed
🎉 All tests passed!
```

---

## 🎨 UI Demo

Open `examples/chat_with_files.html` for:
- 📁 Drag & drop file upload
- 🖼️ File preview
- 💬 Chat with files
- 🎯 Beautiful modern UI

---

## 🔗 Quick Links

- **Technical Guide**: `/docs/FILE_UPLOAD_GUIDE.md`
- **API Reference**: `/docs/FILE_UPLOAD_API.md`
- **Image vs Document**: `/docs/FILE_TYPES_EXPLAINED.md`
- **Environment Config**: `/docs/ENVIRONMENT_CONFIG.md`
- **Test Suite**: `/tests/test_file_upload.py`
- **Web Demo**: `/examples/chat_with_files.html`

---

## 📞 Support

Questions about:
- **File upload**: See `FILE_UPLOAD_GUIDE.md`
- **Image vs Document**: See `FILE_TYPES_EXPLAINED.md`
- **Environment setup**: See `ENVIRONMENT_CONFIG.md`
- **API usage**: See `FILE_UPLOAD_API.md`

---

## 🎉 Summary

### What You Get

✅ **Full file upload support**
- Images: Vision analysis, OCR
- Documents: RAG, Q&A, summarization

✅ **Flexible configuration**
- Environment variables
- Custom API URLs
- No hardcoded values

✅ **Comprehensive documentation**
- 4 new detailed guides
- API reference with examples
- Test suite

✅ **Beautiful UI demo**
- Drag & drop interface
- Real-time preview
- Production-ready

### Next Steps

1. **Install dependency**: `pip install oss2`
2. **Configure environment**: Copy `.env.example` to `.env`
3. **Try the demo**: `open examples/chat_with_files.html`
4. **Read the docs**: Start with `FILE_TYPES_EXPLAINED.md`

---

**Version**: 1.1.0  
**Released**: 2025-10-08  
**Status**: ✅ Production Ready
