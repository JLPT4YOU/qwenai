"""Final test with proper output capture"""
import os
import sys
import uuid
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🖼️  TEST 1: Chat with Image (with output)")
print("=" * 80)

# Upload image
print("\n📤 Uploading image...")
image_metadata = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
print(f"✓ Uploaded: {image_metadata['name']}")

# Create chat and send message
chat_id = str(uuid.uuid4())
message_data = {
    "role": "user",
    "content": "Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
    "files": [image_metadata]
}

print("\n💬 Sending message to AI...")
print("Question: Mô tả chi tiết tấm ảnh này. Đây là ảnh gì?\n")
print("AI Response:")
print("-" * 80)

# Use chat method instead to see streaming output
try:
    # Capture stdout
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Send message with streaming
    result = client.send_message(
        chat_id=chat_id,
        message=message_data,
        model="qwen3-max",
        stream=True
    )
    
    # Get captured output
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    # Print the output
    if output:
        print(output)
    else:
        print("(No streaming output captured)")
    
    # Print result
    if result and result.get('content'):
        print("\n" + "-" * 80)
        print("Final content:", result['content'])
    
except Exception as e:
    sys.stdout = old_stdout
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("📄 TEST 2: Chat with PDF (with output)")
print("=" * 80)

# Upload PDF
print("\n📤 Uploading PDF...")
pdf_metadata = client.upload_file("Đề N3 7-2015-13-15.pdf", filetype="file")
print(f"✓ Uploaded: {pdf_metadata['name']}")

# Create chat and send message
chat_id2 = str(uuid.uuid4())
message_data2 = {
    "role": "user",
    "content": "Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
    "files": [pdf_metadata]
}

print("\n💬 Sending message to AI...")
print("Question: Đây là đề thi gì? Tóm tắt nội dung\n")
print("AI Response:")
print("-" * 80)

try:
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    # Send message with streaming
    result = client.send_message(
        chat_id=chat_id2,
        message=message_data2,
        model="qwen3-max",
        stream=True
    )
    
    # Get captured output
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    # Print the output
    if output:
        print(output)
    else:
        print("(No streaming output captured)")
    
    # Print result
    if result and result.get('content'):
        print("\n" + "-" * 80)
        print("Final content:", result['content'])
    
except Exception as e:
    sys.stdout = old_stdout
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("🎯 TEST 3: Both files together")
print("=" * 80)

chat_id3 = str(uuid.uuid4())
message_data3 = {
    "role": "user",
    "content": "Tôi có 2 file: 1 ảnh và 1 PDF. Hãy phân tích cả 2 và cho biết chúng có liên quan gì đến nhau không? Cả 2 đều liên quan đến học tiếng Nhật phải không?",
    "files": [image_metadata, pdf_metadata]
}

print("\n💬 Sending message with both files...")
print("Question: Phân tích mối liên hệ giữa ảnh và PDF\n")
print("AI Response:")
print("-" * 80)

try:
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    result = client.send_message(
        chat_id=chat_id3,
        message=message_data3,
        model="qwen3-max",
        stream=True
    )
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    if output:
        print(output)
    else:
        print("(No streaming output captured)")
    
    if result and result.get('content'):
        print("\n" + "-" * 80)
        print("Final content:", result['content'])
    
except Exception as e:
    sys.stdout = old_stdout
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ All tests completed!")
print("=" * 80)
