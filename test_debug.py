"""Debug test"""
import os
import sys
import uuid
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🖼️  Upload and Chat with Image")
print("=" * 80)

# Step 1: Upload file
print("\n1. Uploading image...")
file_metadata = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
print(f"✓ Uploaded: {file_metadata['name']}")
print(f"  ID: {file_metadata['id']}")
print(f"  URL: {file_metadata['url'][:80]}...")

# Step 2: Create chat
chat_id = str(uuid.uuid4())
print(f"\n2. Creating chat: {chat_id}")

# Step 3: Send message
print("\n3. Sending message...")
message_data = {
    "role": "user",
    "content": "Mô tả chi tiết tấm ảnh này. Đây là ảnh gì?",
    "files": [file_metadata]
}

print("\n4. Calling send_message...")
try:
    response = client.send_message(
        chat_id=chat_id,
        message=message_data,
        model="qwen3-max",
        stream=True
    )
    
    print("\n5. Response:")
    print(response)
    
    if isinstance(response, dict):
        print(f"\nContent: {response.get('content', 'NO CONTENT')}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("📄 Upload and Chat with PDF")
print("=" * 80)

# Upload PDF
print("\n1. Uploading PDF...")
pdf_metadata = client.upload_file("Đề N3 7-2015-13-15.pdf", filetype="file")
print(f"✓ Uploaded: {pdf_metadata['name']}")
print(f"  ID: {pdf_metadata['id']}")

# Send message
chat_id2 = str(uuid.uuid4())
print(f"\n2. Creating chat: {chat_id2}")

message_data2 = {
    "role": "user",
    "content": "Đây là đề thi gì? Tóm tắt nội dung.",
    "files": [pdf_metadata]
}

print("\n3. Sending message...")
try:
    response2 = client.send_message(
        chat_id=chat_id2,
        message=message_data2,
        model="qwen3-max",
        stream=True
    )
    
    print("\n4. Response:")
    print(response2)
    
    if isinstance(response2, dict):
        print(f"\nContent: {response2.get('content', 'NO CONTENT')}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test completed!")
