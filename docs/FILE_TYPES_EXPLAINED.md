# 📁 File Types: Image vs Document - Chi tiết

## 🎯 Tổng quan

Qwen API hỗ trợ 2 loại file khác nhau với cách xử lý và use case riêng biệt.

---

## 📊 So sánh Image vs Document

| Tiêu chí | **Image** (`filetype: "image"`) | **Document** (`filetype: "file"`) |
|----------|--------------------------------|----------------------------------|
| **Formats** | PNG, JPG, JPEG, GIF, WebP, BMP | PDF, TXT, DOCX, XLSX, PPTX, MD, CSV |
| **Max Size** | 10MB | 50MB |
| **File Class** | `"vision"` | `"document"` |
| **Processing** | Computer Vision (OCR, object detection) | Text extraction, RAG, semantic search |
| **Models** | `qwen3-max`, `qwen-vl-max`, `qwen-vl-plus` | All models |
| **Response Time** | Fast (vision inference) | Slower (document parsing + RAG) |
| **Use Cases** | Visual Q&A, OCR, image analysis | Document Q&A, summarization, extraction |

---

## 🖼️ Image Files (`filetype: "image"`)

### Đặc điểm

```json
{
  "type": "image",
  "file_class": "vision",
  "file_type": "image/png",
  "showType": "image"
}
```

### Cách xử lý

1. **Upload** → Alibaba OSS
2. **Vision Model** → Phân tích nội dung hình ảnh
3. **Response** → Mô tả, OCR text, object detection

### Use Cases

#### 1. **OCR - Đọc text từ ảnh**
```python
client.chat_with_files(
    message="Đọc text trong ảnh này",
    files=["screenshot.png"],
    model="qwen3-max"
)
```

**Example Response:**
```
"Ảnh chứa text: 'N1 Kanji 800' - Đây là trang bìa của một cuốn sách 
học Kanji trình độ N1 với 800 chữ Hán..."
```

#### 2. **Visual Q&A**
```python
client.chat_with_files(
    message="Có bao nhiêu người trong ảnh?",
    files=["photo.jpg"],
    model="qwen-vl-max"
)
```

#### 3. **Image Description**
```python
client.chat_with_files(
    message="Mô tả chi tiết ảnh này",
    files=["landscape.jpg"]
)
```

#### 4. **Object Detection**
```python
client.chat_with_files(
    message="Liệt kê tất cả vật thể trong ảnh",
    files=["room.jpg"]
)
```

### Supported Formats

- **PNG** - Best for screenshots, diagrams
- **JPG/JPEG** - Best for photos
- **GIF** - Animated images (first frame analyzed)
- **WebP** - Modern format, smaller size
- **BMP** - Uncompressed, large files

### Limitations

- Max 10MB per image
- Animated GIFs: Only first frame analyzed
- Very high resolution images may be downscaled
- NSFW content will be blocked by greenNet

---

## 📄 Document Files (`filetype: "file"`)

### Đặc điểm

```json
{
  "type": "file",
  "file_class": "document",
  "file_type": "application/pdf",
  "showType": "file"
}
```

### Cách xử lý

1. **Upload** → Alibaba OSS
2. **Document Parser** → Extract text, structure
3. **RAG System** → Index content, semantic search
4. **LLM** → Answer questions based on content

### Use Cases

#### 1. **Document Q&A**
```python
client.chat_with_files(
    message="Cuốn sách này nói về gì?",
    files=["N1Kanji800.pdf"],
    model="qwen3-max"
)
```

**Example Response:**
```
"Cuốn sách 'N1 Kanji 800' là tài liệu học tiếng Nhật trình độ N1, 
tập trung vào 800 chữ Hán thường gặp trong kỳ thi JLPT N1. 
Sách bao gồm:
- Danh sách 800 Kanji theo độ khó
- Cách đọc On và Kun
- Ví dụ câu sử dụng
- Bài tập luyện tập..."
```

#### 2. **Summarization**
```python
client.chat_with_files(
    message="Tóm tắt nội dung chính của tài liệu",
    files=["report.pdf"]
)
```

#### 3. **Information Extraction**
```python
client.chat_with_files(
    message="Liệt kê tất cả các số liệu quan trọng trong báo cáo",
    files=["financial_report.xlsx"]
)
```

#### 4. **Multi-document Analysis**
```python
client.chat_with_files(
    message="So sánh nội dung của 2 tài liệu này",
    files=["doc1.pdf", "doc2.pdf"]
)
```

#### 5. **Code Analysis**
```python
client.chat_with_files(
    message="Giải thích code trong file này",
    files=["script.py"]
)
```

### Supported Formats

- **PDF** - Best for books, reports, forms
- **TXT** - Plain text files
- **DOCX** - Microsoft Word documents
- **XLSX** - Excel spreadsheets
- **PPTX** - PowerPoint presentations
- **MD** - Markdown files
- **CSV** - Data tables
- **JSON** - Structured data

### Limitations

- Max 50MB per document
- PDF: Max 1000 pages
- Password-protected files not supported
- Scanned PDFs: OCR quality depends on scan quality
- Complex layouts may affect parsing accuracy

---

## 🔄 Auto-detection

Nếu không chỉ định `filetype`, hệ thống tự động detect:

```python
# Auto-detect based on MIME type
client.upload_file("image.png")  # → filetype="image"
client.upload_file("document.pdf")  # → filetype="file"
```

**Detection Logic:**
```python
import mimetypes

mime_type, _ = mimetypes.guess_type(file_path)
if mime_type and mime_type.startswith('image/'):
    filetype = "image"
else:
    filetype = "file"
```

---

## 💡 Best Practices

### Khi nào dùng Image?

✅ **Dùng Image khi:**
- Cần OCR text từ ảnh chụp
- Phân tích visual content (màu sắc, layout, objects)
- Đọc biển báo, menu, screenshot UI
- So sánh hình ảnh
- Detect objects, faces, scenes

❌ **Không dùng Image khi:**
- File là PDF text-based (dùng document sẽ tốt hơn)
- Cần extract structured data
- Document có nhiều trang

### Khi nào dùng Document?

✅ **Dùng Document khi:**
- Cần đọc và phân tích nội dung text
- Extract thông tin từ PDF, Word, Excel
- Q&A over long documents
- Summarize reports, books
- Code analysis

❌ **Không dùng Document khi:**
- File là ảnh chụp (dùng image để OCR)
- Cần visual analysis
- File là infographic (dùng image)

---

## 🎯 Examples từ thực tế

### Example 1: PDF Scan vs PDF Text

**Scenario:** Bạn có PDF của cuốn sách N1 Kanji

**Option A: Upload as Image** (nếu PDF là scan)
```python
# Convert PDF pages to images first
from pdf2image import convert_from_path

images = convert_from_path("N1Kanji800.pdf")
images[0].save("page1.png")

# Upload as image
client.chat_with_files(
    message="Đọc nội dung trang này",
    files=["page1.png"],
    filetype="image"
)
```

**Option B: Upload as Document** (nếu PDF có text layer)
```python
# Upload directly as document
client.chat_with_files(
    message="Cuốn sách này khó không?",
    files=["N1Kanji800.pdf"],
    filetype="file"
)
```

### Example 2: Screenshot vs Text File

**Screenshot của code:**
```python
# Upload as image for OCR
client.chat_with_files(
    message="Giải thích code trong screenshot",
    files=["code_screenshot.png"],
    filetype="image"
)
```

**Source code file:**
```python
# Upload as document for better analysis
client.chat_with_files(
    message="Review code này",
    files=["script.py"],
    filetype="file"
)
```

### Example 3: Mixed Content

**Analyze presentation with images:**
```python
# Upload PPTX as document
client.chat_with_files(
    message="Tóm tắt presentation này",
    files=["slides.pptx"],
    filetype="file"
)

# Extract specific slide as image for visual analysis
client.chat_with_files(
    message="Phân tích biểu đồ trong slide này",
    files=["slide_5_chart.png"],
    filetype="image"
)
```

---

## 🔍 Technical Details

### Image Processing Pipeline

```
Image Upload → OSS Storage → Vision Model
                                  ↓
                          Feature Extraction
                                  ↓
                          OCR + Object Detection
                                  ↓
                          LLM Processing
                                  ↓
                          Response
```

### Document Processing Pipeline

```
Document Upload → OSS Storage → Document Parser
                                      ↓
                                Text Extraction
                                      ↓
                                Chunking + Embedding
                                      ↓
                                Vector Database (RAG)
                                      ↓
                                Semantic Search
                                      ↓
                                LLM Processing
                                      ↓
                                Response
```

---

## 📊 Performance Comparison

| Metric | Image | Document |
|--------|-------|----------|
| **Upload Time** | ~1-3s | ~2-10s (depends on size) |
| **Processing Time** | ~2-5s | ~5-30s (depends on pages) |
| **Token Usage** | Low (vision tokens) | High (text tokens) |
| **Accuracy** | High for visual content | High for text content |
| **Cost** | Lower | Higher (more tokens) |

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Upload PDF scan as document
```python
# Wrong: PDF scan uploaded as document
client.upload_file("scanned_book.pdf", filetype="file")
# → Poor text extraction, low accuracy
```

**✅ Correct:**
```python
# Convert to images first
client.upload_file("page1.png", filetype="image")
# → Better OCR, higher accuracy
```

### ❌ Mistake 2: Upload text-based PDF as image
```python
# Wrong: Text PDF as image
client.upload_file("text_document.pdf", filetype="image")
# → Only first page analyzed as image
```

**✅ Correct:**
```python
# Upload as document
client.upload_file("text_document.pdf", filetype="file")
# → Full document indexed and searchable
```

### ❌ Mistake 3: Large image file
```python
# Wrong: 15MB photo
client.upload_file("huge_photo.jpg", filetype="image")
# → Error: File too large
```

**✅ Correct:**
```python
# Resize first
from PIL import Image
img = Image.open("huge_photo.jpg")
img.thumbnail((2000, 2000))
img.save("resized.jpg")
client.upload_file("resized.jpg", filetype="image")
```

---

## 📝 Summary

### Image (`filetype: "image"`)
- 🎯 **Purpose**: Visual analysis, OCR, object detection
- 📏 **Size**: Max 10MB
- 🤖 **Models**: Vision models
- ⚡ **Speed**: Fast
- 💰 **Cost**: Lower

### Document (`filetype: "file"`)
- 🎯 **Purpose**: Text analysis, Q&A, summarization
- 📏 **Size**: Max 50MB
- 🤖 **Models**: All models
- ⚡ **Speed**: Slower (RAG processing)
- 💰 **Cost**: Higher

**Rule of thumb:**
- Visual content → Image
- Text content → Document
- Mixed content → Both (separate uploads)

---

## 🔗 Related Documentation

- **Upload Guide**: `/docs/FILE_UPLOAD_GUIDE.md`
- **API Reference**: `/docs/FILE_UPLOAD_API.md`
- **Examples**: `/examples/chat_with_files.html`
