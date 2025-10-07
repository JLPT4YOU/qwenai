# 🎯 System Prompt / Instructions - Hướng Dẫn

## 🔍 Tìm Hiểu Cách Qwen Xử Lý Instructions

### Phương Pháp Tìm Kiếm

**Bước 1: Check trong Browser**

1. Mở https://chat.qwen.ai
2. Press F12 → Network tab
3. Filter: Fetch/XHR
4. Tạo chat mới hoặc gửi message
5. Check request payload

**Bước 2: Tìm Settings/Configuration**

Trong Qwen web interface, tìm:
- ⚙️ Settings icon
- 📝 Prompt/Instruction settings
- 🤖 Model configuration
- 💬 Chat settings

### 📊 Test Results (Sơ Bộ)

| Method | Status | Works? | Notes |
|--------|--------|--------|-------|
| System message in array | ❌ Timeout | No | Không support |
| `system_prompt` field | ⚠️ 200 | Maybe | Cần test thêm |
| `instruction` field | ⚠️ 200 | Maybe | Cần test thêm |
| Inline in message | ✅ 200 | Yes | Simplest |

---

## ✅ Giải Pháp Tạm Thời: Inline Instructions

Trong khi chờ tìm hiểu chính thức, bạn có thể dùng **inline instructions** trong message:

### Phương Pháp 1: Prefix Instructions

```python
def send_with_instruction(client, chat_id, instruction, message):
    """Send message with instruction prefix"""
    full_message = f"""[INSTRUCTION]
{instruction}

[USER MESSAGE]
{message}
"""
    return client.send_message(chat_id, full_message)
```

**Example:**
```python
instruction = """Bạn là một chuyên gia lập trình Python.
- Luôn giải thích code rõ ràng
- Đưa ví dụ cụ thể
- Sử dụng best practices"""

message = "Làm thế nào để đọc file CSV?"

send_with_instruction(client, chat_id, instruction, message)
```

### Phương Pháp 2: Hidden System Prompt

```python
# Gửi system prompt ở đầu conversation
client.send_message(chat_id, """
🤖 SYSTEM CONFIGURATION:
- Bạn là trợ lý AI chuyên về lập trình
- Luôn trả lời bằng tiếng Việt
- Code examples phải có comment
- Giải thích ngắn gọn, dễ hiểu

[Đã hiểu. Tôi sẵn sàng giúp đỡ!]
""")

# Sau đó chat bình thường
client.send_message(chat_id, "Viết function đọc JSON file")
```

### Phương Pháp 3: Role-Playing

```python
message = """
Hãy hành động như một giáo viên Python kinh nghiệm.
Nhiệm vụ của bạn là giải thích code đơn giản cho người mới bắt đầu.

Câu hỏi: Làm thế nào để sử dụng list comprehension?
"""
```

---

## 🔧 Implementation trong Code

### Update `qwen_client.py`

```python
def send_message(
    self,
    chat_id: str,
    message: str,
    model: str = "qwen3-max",
    parent_id: Optional[str] = None,
    stream: bool = True,
    system_prompt: Optional[str] = None  # ← New parameter
) -> Dict:
    """
    Send a message with optional system prompt
    
    Args:
        system_prompt: Optional instruction/system prompt to prepend
    """
    
    # If system prompt provided, prepend it
    if system_prompt:
        message = f"""[INSTRUCTION]
{system_prompt}

[MESSAGE]
{message}
"""
    
    # Rest of the code remains the same
    ...
```

### Update `api_server.py`

```python
@app.route('/api/chat/send', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_id = data.get('chat_id')
    message = data.get('message')
    system_prompt = data.get('system_prompt')  # ← New field
    
    # ... (get client)
    
    response = client.send_message(
        chat_id=chat_id,
        message=message,
        system_prompt=system_prompt  # ← Pass through
    )
```

### Update `index_v2.html`

```html
<div class="settings-panel">
    <label>System Prompt (Optional):</label>
    <textarea id="systemPrompt" placeholder="Enter instructions for AI..."></textarea>
</div>

<script>
async function sendMessage() {
    const message = document.getElementById('messageInput').value;
    const systemPrompt = document.getElementById('systemPrompt').value;
    
    const response = await fetch(`${API_BASE}/chat/send`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${AUTH_TOKEN}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            chat_id: CURRENT_CHAT_ID,
            message: message,
            system_prompt: systemPrompt || null
        })
    });
}
</script>
```

---

## 🎓 Best Practices cho Instructions

### 1. Rõ Ràng và Cụ Thể

❌ **Bad:**
```
Trả lời tốt
```

✅ **Good:**
```
- Trả lời bằng tiếng Việt
- Giải thích theo từng bước
- Đưa ví dụ code khi cần
- Độ dài: 2-3 đoạn văn
```

### 2. Định Nghĩa Role

```
Bạn là một [ROLE]:
- [Characteristic 1]
- [Characteristic 2]
- [Constraint 1]

Nhiệm vụ: [TASK]
```

**Example:**
```
Bạn là một senior Python developer:
- 10+ năm kinh nghiệm
- Chuyên về data science và ML
- Luôn follow PEP 8
- Giải thích code cho beginners

Nhiệm vụ: Hướng dẫn học Python từ cơ bản đến nâng cao
```

### 3. Output Format

```
Format output:
- Tiêu đề: **Bold**
- Code: ```python ... ```
- Examples: Ít nhất 2 ví dụ
- Giải thích: Ngắn gọn, dễ hiểu
```

### 4. Constraints

```
Ràng buộc:
- Độ dài: Tối đa 200 từ
- Ngôn ngữ: Tiếng Việt 100%
- Code style: PEP 8
- Không dùng: Deprecated functions
```

---

## 📝 Examples

### Example 1: Coding Assistant

```python
system_prompt = """
Bạn là Python Coding Assistant:
- Chuyên gia về Python 3.10+
- Luôn sử dụng type hints
- Code phải có docstring
- Follow PEP 8 style guide
- Giải thích ngắn gọn bằng tiếng Việt

Output format:
1. Code snippet với comments
2. Giải thích cách hoạt động
3. Example usage
"""

client.send_message(
    chat_id,
    "Viết function tính factorial",
    system_prompt=system_prompt
)
```

### Example 2: Vietnamese Tutor

```python
system_prompt = """
Bạn là giáo viên tiếng Việt:
- Giải thích ngữ pháp đơn giản
- Đưa ví dụ thực tế
- Sửa lỗi chính tả
- Gợi ý cách viết hay hơn

Quy tắc:
- Luôn lịch sự, khuyến khích
- Giải thích tại sao sai/đúng
- Đưa 2-3 ví dụ tương tự
"""
```

### Example 3: Data Analyst

```python
system_prompt = """
Bạn là Data Analyst chuyên nghiệp:

Khi phân tích data:
1. Hiểu requirements
2. Suggest approach
3. Provide pandas/numpy code
4. Explain insights

Output bao gồm:
- 📊 Code để load và clean data
- 📈 Visualization suggestions
- 💡 Key insights
- ⚠️ Caveats và limitations
"""
```

---

## 🔍 Cần Tìm Hiểu Thêm

### Browser Developer Tools

1. **Mở Qwen Chat:** https://chat.qwen.ai
2. **Open DevTools:** F12
3. **Network Tab:** Filter XHR/Fetch
4. **Send Message:** Gửi 1 tin nhắn
5. **Check Payload:** Xem request body

**Tìm những field này:**
- `system`
- `instruction`
- `prompt`
- `context`
- `role: "system"`
- `configuration`

### Check Response Structure

```python
import requests

# Send test message
response = requests.post(...)

# Print full response
print(json.dumps(response.json(), indent=2))

# Look for:
# - data structure
# - metadata fields
# - configuration options
```

---

## 🎯 Next Steps

1. **Browser Investigation**
   - Check actual payloads from chat.qwen.ai
   - Find official system prompt field

2. **API Documentation**
   - Search for Qwen API docs
   - Check if there's official documentation

3. **Test Different Approaches**
   - Try conversation history approach
   - Test with different models

4. **Implement in Code**
   - Add system_prompt parameter
   - Update UI với system prompt textbox
   - Test thoroughly

---

## 💡 Temporary Solution (Works Now)

Cho đến khi tìm ra cách chính thức, dùng **inline instructions** là cách đơn giản nhất:

```python
from qwen_client import QwenClient

client = QwenClient(token)
chats = client.list_chats()
chat_id = chats['data'][0]['id']

# Method 1: Direct inline
message = """[INSTRUCTION: Trả lời ngắn gọn, tối đa 2 câu]

Giới thiệu về Python"""

client.send_message(chat_id, message)

# Method 2: Helper function
def chat_with_instruction(instruction, message):
    full_msg = f"[INSTRUCTION]\n{instruction}\n\n[MESSAGE]\n{message}"
    return client.send_message(chat_id, full_msg)

chat_with_instruction(
    "Bạn là chuyên gia Python",
    "Giải thích list comprehension"
)
```

---

**Status:** 🔍 Investigating  
**Temporary Solution:** ✅ Inline instructions work  
**Official Support:** ⏳ Need to find documentation

---

## 📚 Resources

- Qwen Chat: https://chat.qwen.ai
- Qwen Docs: https://help.aliyun.com/zh/dashscope/
- OpenAI Format: https://platform.openai.com/docs/api-reference/chat

**Next:** Check browser DevTools để tìm official method!
