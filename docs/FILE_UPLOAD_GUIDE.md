# Hướng dẫn Upload File & Image - Qwen API

## Tổng quan

Qwen API hỗ trợ upload 2 loại file:
- **Image**: PNG, JPG, JPEG, GIF, WebP (cho vision models)
- **Document**: PDF, TXT, DOCX, etc. (cho RAG/document analysis)

## Flow Upload File

### 1. Lấy STS Token
```http
POST https://chat.qwen.ai/api/v2/files/getstsToken
Authorization: Bearer <token>
Content-Type: application/json

{
  "filename": "example.png",
  "filesize": 545775,
  "filetype": "image"  // hoặc "file" cho documents
}
```

**Response:**
```json
{
  "access_key_id": "STS.xxx",
  "access_key_secret": "xxx",
  "security_token": "CAISxxx...",
  "expiration": "2025-10-08T11:06:48Z",
  "region": "ap-southeast-1",
  "bucket": "qwen-webui-prod",
  "endpoint": "oss-accelerate.aliyuncs.com",
  "file_id": "2d554784-e0ef-4a1d-abc3-f944d9f26cd4",
  "object_key": "f4506b78-a768-4a55-89ac-c5fb61be7a08/2d554784-e0ef-4a1d-abc3-f944d9f26cd4_example.png"
}
```

### 2. Upload File lên OSS
Sử dụng credentials từ bước 1 để upload trực tiếp lên Alibaba OSS:

```python
import oss2
from oss2.credentials import StsAuth

auth = StsAuth(access_key_id, access_key_secret, security_token)
bucket = oss2.Bucket(auth, endpoint, bucket_name)
bucket.put_object(object_key, file_content)
```

### 3. Gửi Message kèm File
```http
POST https://chat.qwen.ai/api/v2/chat/completions?chat_id=<chat_id>
Authorization: Bearer <token>
Content-Type: application/json

{
  "stream": true,
  "chat_id": "36d30933-7152-4281-b903-e9961262c831",
  "model": "qwen3-max",
  "messages": [
    {
      "role": "user",
      "content": "Phân tích hình ảnh này",
      "files": [
        {
          "type": "image",
          "id": "2d554784-e0ef-4a1d-abc3-f944d9f26cd4",
          "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/...",
          "name": "example.png",
          "size": 545775,
          "file_type": "image/png",
          "file_class": "vision",
          "status": "uploaded"
        }
      ]
    }
  ]
}
```

## File Structure trong Message

### Image File
```json
{
  "type": "image",
  "file": {
    "id": "uuid",
    "filename": "screenshot.png",
    "user_id": "user-uuid",
    "meta": {
      "name": "screenshot.png",
      "size": 545775,
      "content_type": "image/png"
    },
    "created_at": 1759885609538
  },
  "id": "uuid",
  "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/...",
  "name": "screenshot.png",
  "size": 545775,
  "file_type": "image/png",
  "showType": "image",
  "file_class": "vision",
  "status": "uploaded",
  "greenNet": "success"
}
```

### Document File (PDF)
```json
{
  "type": "file",
  "file": {
    "id": "uuid",
    "filename": "N1Kanji800.pdf",
    "meta": {
      "name": "N1Kanji800.pdf",
      "size": 18422686,
      "content_type": "application/pdf"
    }
  },
  "id": "uuid",
  "url": "https://qwen-webui-prod.oss-accelerate.aliyuncs.com/...",
  "name": "N1Kanji800.pdf",
  "size": 18422686,
  "file_type": "application/pdf",
  "file_class": "document",
  "status": "uploaded"
}
```

## Lưu ý quan trọng

### 1. File Type Mapping
- `filetype: "image"` → `file_class: "vision"` → Dùng cho vision models
- `filetype: "file"` → `file_class: "document"` → Dùng cho document analysis

### 2. Model Support
- **Vision models**: `qwen3-max`, `qwen-vl-max`, `qwen-vl-plus`
- **Document models**: Tất cả models hỗ trợ RAG

### 3. File Size Limits
- **Image**: Max 10MB
- **Document**: Max 50MB
- **Total per message**: Max 100MB

### 4. Supported Formats
**Images:**
- PNG, JPG, JPEG, GIF, WebP, BMP
- Recommended: PNG hoặc JPG

**Documents:**
- PDF, TXT, DOCX, XLSX, PPTX
- Markdown, CSV, JSON

### 5. Security
- STS token có thời hạn 5 phút (300s)
- Signed URL có thời hạn 5 phút
- File được scan bởi "greenNet" (content moderation)

## Implementation trong Python

### Upload Image Example
```python
import requests
import uuid
from pathlib import Path

def upload_image(token: str, image_path: str) -> dict:
    """Upload image và trả về file metadata"""
    
    # 1. Đọc file
    file_path = Path(image_path)
    file_size = file_path.stat().st_size
    
    # 2. Lấy STS token
    response = requests.post(
        "https://chat.qwen.ai/api/v2/files/getstsToken",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "filename": file_path.name,
            "filesize": file_size,
            "filetype": "image"
        }
    )
    sts_data = response.json()
    
    # 3. Upload lên OSS
    import oss2
    from oss2.credentials import StsAuth
    
    auth = StsAuth(
        sts_data['access_key_id'],
        sts_data['access_key_secret'],
        sts_data['security_token']
    )
    bucket = oss2.Bucket(
        auth,
        f"https://{sts_data['endpoint']}",
        sts_data['bucket']
    )
    
    with open(image_path, 'rb') as f:
        bucket.put_object(sts_data['object_key'], f)
    
    # 4. Tạo file metadata
    file_url = f"https://{sts_data['bucket']}.{sts_data['endpoint']}/{sts_data['object_key']}"
    
    return {
        "type": "image",
        "id": sts_data['file_id'],
        "url": file_url,
        "name": file_path.name,
        "size": file_size,
        "file_type": "image/png",
        "file_class": "vision",
        "status": "uploaded"
    }

def send_message_with_image(token: str, chat_id: str, content: str, image_path: str):
    """Gửi message kèm image"""
    
    # Upload image
    file_metadata = upload_image(token, image_path)
    
    # Gửi message
    response = requests.post(
        f"https://chat.qwen.ai/api/v2/chat/completions?chat_id={chat_id}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "stream": True,
            "chat_id": chat_id,
            "model": "qwen3-max",
            "messages": [{
                "role": "user",
                "content": content,
                "files": [file_metadata]
            }]
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
```

## Troubleshooting

### Error: "File too large"
- Giảm kích thước file
- Compress image trước khi upload

### Error: "Invalid file type"
- Kiểm tra extension file
- Đảm bảo `filetype` đúng ("image" hoặc "file")

### Error: "STS token expired"
- Token chỉ có hiệu lực 5 phút
- Upload ngay sau khi lấy token

### Error: "greenNet failed"
- File vi phạm content policy
- Thử file khác

## Best Practices

1. **Validate file trước khi upload**
   - Check file size
   - Check file type
   - Scan for malware

2. **Handle errors gracefully**
   - Retry logic cho network errors
   - Clear error messages cho users

3. **Optimize images**
   - Resize large images
   - Convert to WebP cho file size nhỏ hơn

4. **Cache file metadata**
   - Lưu file_id và url để reuse
   - Tránh upload lại cùng file

5. **Progress tracking**
   - Show upload progress
   - Allow cancel upload
