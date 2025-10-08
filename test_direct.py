"""Direct test - no output capture"""
import os
import uuid
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🖼️  TEST: Chat with Image - Direct Output")
print("=" * 80)

# Upload image
print("\n📤 Uploading image...")
image_metadata = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
print(f"✓ Uploaded: {image_metadata['name']}")
print(f"  File ID: {image_metadata['id']}")

# Create chat
chat_id = str(uuid.uuid4())
print(f"\n💬 Chat ID: {chat_id}")

# Prepare message
message_data = {
    "role": "user",
    "content": "Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
    "files": [image_metadata]
}

print("\n📝 Message content:", message_data['content'])
print(f"📎 Files attached: {len(message_data['files'])}")
print(f"   - {message_data['files'][0]['name']} ({message_data['files'][0]['file_class']})")

print("\n🤖 AI Response (streaming):")
print("-" * 80)

# Send with streaming - output should print directly
result = client.send_message(
    chat_id=chat_id,
    message=message_data,
    model="qwen3-max",
    stream=True
)

print("\n" + "-" * 80)
print(f"\n📊 Result type: {type(result)}")
print(f"📊 Result keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
print(f"📊 Content length: {len(result.get('content', '')) if isinstance(result, dict) else 0}")

if isinstance(result, dict) and result.get('content'):
    print(f"\n✅ Final content:\n{result['content']}")
else:
    print("\n⚠️  No content in result")

print("\n" + "=" * 80)
