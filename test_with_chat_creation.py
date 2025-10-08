"""Test with proper chat creation"""
import requests
import json
import uuid
import time

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

# Upload file
from qwen_client import QwenClient
client = QwenClient(auth_token=token)

print("=" * 80)
print("🧪 Complete Test with Chat Creation")
print("=" * 80)

print("\n1. Uploading image...")
file_metadata = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
print(f"✓ File ID: {file_metadata['id']}")
print(f"  File class: {file_metadata['file_class']}")

# Create chat first
print("\n2. Creating chat...")
chat_data = client.create_chat()
chat_id = chat_data.get('id')
print(f"✓ Chat ID: {chat_id}")

# Now send message with file
print("\n3. Sending message with file...")
print("Question: Mô tả chi tiết tấm ảnh này\n")

message_data = {
    "role": "user",
    "content": "Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
    "files": [file_metadata]
}

print("🤖 AI Response:")
print("-" * 80)

result = client.send_message(
    chat_id=chat_id,
    message=message_data,
    model="qwen3-max",
    stream=True
)

print("\n" + "-" * 80)

if isinstance(result, dict):
    if result.get('content'):
        print(f"\n✅ Content received ({len(result['content'])} chars)")
    else:
        print("\n⚠️  No content in response")
        print(f"Result: {result}")

print("\n" + "=" * 80)
print("📄 TEST 2: PDF")
print("=" * 80)

print("\n1. Uploading PDF...")
pdf_metadata = client.upload_file("Đề N3 7-2015-13-15.pdf", filetype="file")
print(f"✓ File ID: {pdf_metadata['id']}")

print("\n2. Creating new chat...")
chat_data2 = client.create_chat()
chat_id2 = chat_data2.get('id')
print(f"✓ Chat ID: {chat_id2}")

print("\n3. Sending message with PDF...")
print("Question: Đây là đề thi gì?\n")

message_data2 = {
    "role": "user",
    "content": "Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
    "files": [pdf_metadata]
}

print("🤖 AI Response:")
print("-" * 80)

result2 = client.send_message(
    chat_id=chat_id2,
    message=message_data2,
    model="qwen3-max",
    stream=True
)

print("\n" + "-" * 80)

if isinstance(result2, dict):
    if result2.get('content'):
        print(f"\n✅ Content received ({len(result2['content'])} chars)")
    else:
        print("\n⚠️  No content in response")

print("\n✅ Test completed!")
