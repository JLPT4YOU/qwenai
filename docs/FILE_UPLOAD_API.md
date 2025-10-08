# File Upload API Documentation

## Overview

Qwen API hỗ trợ upload và xử lý file (images & documents) thông qua 3 endpoints chính.

## Endpoints

### 1. Get STS Token

Lấy temporary credentials để upload file lên Alibaba OSS.

```http
POST /api/files/sts-token
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "filename": "example.png",
  "filesize": 545775,
  "filetype": "image"
}
```

**Parameters:**
- `filename` (string, required): Tên file
- `filesize` (number, required): Kích thước file (bytes)
- `filetype` (string, required): Loại file - `"image"` hoặc `"file"`

**Response:**
```json
{
  "success": true,
  "data": {
    "access_key_id": "STS.xxx",
    "access_key_secret": "xxx",
    "security_token": "CAISxxx...",
    "expiration": "2025-10-08T11:06:48Z",
    "region": "ap-southeast-1",
    "bucket": "qwen-webui-prod",
    "endpoint": "oss-accelerate.aliyuncs.com",
    "file_id": "uuid",
    "object_key": "user_id/file_id_filename.ext"
  }
}
```

---

### 2. Upload File

Upload file hoàn chỉnh (tự động lấy STS token và upload lên OSS).

```http
POST /api/files/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file` (file, required): File cần upload
- `filetype` (string, optional): `"image"` hoặc `"file"` (auto-detect nếu không có)

**Example (curl):**
```bash
curl -X POST http://localhost:5001/api/files/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "filetype=image"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "type": "image",
    "id": "uuid",
    "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/...",
    "name": "image.png",
    "size": 545775,
    "file_type": "image/png",
    "file_class": "vision",
    "status": "uploaded"
  }
}
```

---

### 3. Send Message with Files

Gửi message kèm file attachments.

```http
POST /api/chat/send-with-files
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `message` (string, required): Nội dung message
- `files` (file[], required): Một hoặc nhiều files
- `chat_id` (string, optional): Chat ID (tạo mới nếu không có)
- `model` (string, optional): Model name (default: `qwen3-max`)

**Example (curl):**
```bash
curl -X POST http://localhost:5001/api/chat/send-with-files \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "message=What do you see in this image?" \
  -F "files=@/path/to/image1.png" \
  -F "files=@/path/to/image2.jpg" \
  -F "model=qwen3-max"
```

**Response:**
```json
{
  "success": true,
  "chat_id": "uuid",
  "data": {
    "content": "AI's response about the images..."
  }
}
```

---

## Python Examples

### Example 1: Upload Single Image

```python
import requests

token = "your_token_here"
api_url = "http://localhost:5001"

# Upload image
with open("image.png", "rb") as f:
    response = requests.post(
        f"{api_url}/api/files/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("image.png", f, "image/png")},
        data={"filetype": "image"}
    )

file_data = response.json()
print(f"File uploaded: {file_data['data']['url']}")
```

### Example 2: Chat with Image

```python
import requests

token = "your_token_here"
api_url = "http://localhost:5001"

# Send message with image
with open("screenshot.png", "rb") as f:
    response = requests.post(
        f"{api_url}/api/chat/send-with-files",
        headers={"Authorization": f"Bearer {token}"},
        files={"files": ("screenshot.png", f, "image/png")},
        data={
            "message": "Analyze this screenshot",
            "model": "qwen3-max"
        }
    )

result = response.json()
print(f"AI Response: {result['data']['content']}")
```

### Example 3: Chat with Multiple Files

```python
import requests

token = "your_token_here"
api_url = "http://localhost:5001"

files_to_upload = [
    ("files", ("image1.png", open("image1.png", "rb"), "image/png")),
    ("files", ("image2.jpg", open("image2.jpg", "rb"), "image/jpeg")),
    ("files", ("document.pdf", open("document.pdf", "rb"), "application/pdf"))
]

response = requests.post(
    f"{api_url}/api/chat/send-with-files",
    headers={"Authorization": f"Bearer {token}"},
    files=files_to_upload,
    data={
        "message": "Compare these images and summarize the document",
        "model": "qwen3-max"
    }
)

result = response.json()
print(f"AI Response: {result['data']['content']}")

# Close files
for _, (_, file_obj, _) in files_to_upload:
    file_obj.close()
```

### Example 4: Using QwenClient

```python
from qwen_client import QwenClient

client = QwenClient(auth_token="your_token_here")

# Upload and chat with files
response = client.chat_with_files(
    message="What's in these images?",
    files=["image1.png", "image2.jpg"],
    model="qwen3-max"
)

print(response['content'])
```

---

## JavaScript Examples

### Example 1: Upload File from Browser

```javascript
async function uploadFile(file, token) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('filetype', file.type.startsWith('image/') ? 'image' : 'file');

    const response = await fetch('http://localhost:5001/api/files/upload', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();
    return data.data;
}

// Usage
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];
const fileData = await uploadFile(file, 'your_token_here');
console.log('Uploaded:', fileData.url);
```

### Example 2: Send Message with Files

```javascript
async function sendMessageWithFiles(message, files, token) {
    const formData = new FormData();
    formData.append('message', message);
    formData.append('model', 'qwen3-max');

    files.forEach(file => {
        formData.append('files', file);
    });

    const response = await fetch('http://localhost:5001/api/chat/send-with-files', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });

    const data = await response.json();
    return data.data;
}

// Usage
const fileInput = document.getElementById('fileInput');
const files = Array.from(fileInput.files);
const response = await sendMessageWithFiles(
    'Analyze these images',
    files,
    'your_token_here'
);
console.log('AI Response:', response.content);
```

---

## File Type Support

### Images (filetype: "image")
- **Formats**: PNG, JPG, JPEG, GIF, WebP, BMP
- **Max Size**: 10MB
- **Use Case**: Vision analysis, OCR, image understanding
- **Models**: `qwen3-max`, `qwen-vl-max`, `qwen-vl-plus`

### Documents (filetype: "file")
- **Formats**: PDF, TXT, DOCX, XLSX, PPTX, MD, CSV, JSON
- **Max Size**: 50MB
- **Use Case**: Document analysis, RAG, text extraction
- **Models**: All models support document processing

---

## Error Handling

### Common Errors

**401 Unauthorized**
```json
{
  "error": "No authorization token"
}
```
→ Token không hợp lệ hoặc thiếu

**400 Bad Request**
```json
{
  "error": "No file provided"
}
```
→ Thiếu file trong request

**403 Forbidden**
```json
{
  "error": "Access denied: Invalid origin"
}
```
→ CORS error, kiểm tra origin

**500 Internal Server Error**
```json
{
  "error": "oss2 package required. Install with: pip install oss2"
}
```
→ Thiếu dependency, chạy `pip install oss2`

---

## Best Practices

### 1. File Validation
```python
def validate_file(file_path):
    """Validate file before upload"""
    import os
    from pathlib import Path
    
    # Check file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file size
    size = os.path.getsize(file_path)
    max_size = 10 * 1024 * 1024  # 10MB for images
    
    if size > max_size:
        raise ValueError(f"File too large: {size} bytes (max: {max_size})")
    
    # Check file extension
    ext = Path(file_path).suffix.lower()
    allowed_exts = ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.txt']
    
    if ext not in allowed_exts:
        raise ValueError(f"Unsupported file type: {ext}")
    
    return True
```

### 2. Progress Tracking
```python
def upload_with_progress(file_path, token):
    """Upload file with progress tracking"""
    import os
    from tqdm import tqdm
    
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
            # Upload logic here
            pbar.update(file_size)
```

### 3. Error Retry
```python
def upload_with_retry(file_path, token, max_retries=3):
    """Upload with automatic retry"""
    import time
    
    for attempt in range(max_retries):
        try:
            return client.upload_file(file_path)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

### 4. Batch Upload
```python
def upload_multiple_files(file_paths, token):
    """Upload multiple files efficiently"""
    from concurrent.futures import ThreadPoolExecutor
    
    client = QwenClient(auth_token=token)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(client.upload_file, file_paths))
    
    return results
```

---

## Testing

Chạy test suite:

```bash
# Install dependencies
pip install oss2

# Run tests
python tests/test_file_upload.py
```

Test coverage:
- ✅ Get STS token
- ✅ Upload image file
- ✅ Upload document file
- ✅ Chat with image
- ✅ API endpoint upload
- ✅ Multiple files upload

---

## Security Notes

1. **Token Security**: Không hardcode token trong code, dùng environment variables
2. **File Validation**: Luôn validate file type và size trước khi upload
3. **CORS**: API server có CORS protection, chỉ cho phép trusted origins
4. **Content Moderation**: Files được scan bởi "greenNet" system
5. **STS Token**: Temporary credentials có hiệu lực 5 phút

---

## Troubleshooting

### Issue: "oss2 package required"
**Solution:**
```bash
pip install oss2
```

### Issue: "File too large"
**Solution:** Compress file hoặc resize image trước khi upload

### Issue: "STS token expired"
**Solution:** Token chỉ có hiệu lực 5 phút, upload ngay sau khi lấy token

### Issue: "CORS error"
**Solution:** Kiểm tra API server CORS config trong `api_server.py`

### Issue: "greenNet failed"
**Solution:** File vi phạm content policy, thử file khác

---

## Demo

Mở file HTML demo:
```bash
open examples/chat_with_files.html
```

Hoặc truy cập: `file:///path/to/examples/chat_with_files.html`

---

## Support

- **Documentation**: `/docs/FILE_UPLOAD_GUIDE.md`
- **API Reference**: `/docs/FILE_UPLOAD_API.md`
- **Examples**: `/examples/chat_with_files.html`
- **Tests**: `/tests/test_file_upload.py`
