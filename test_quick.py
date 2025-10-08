"""Quick test with streaming"""
import os
from qwen_client import QwenClient

token = os.getenv("QWEN_TOKEN") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🖼️  TEST: Chat with Image (Streaming)")
print("=" * 80)

print("\n📤 Uploading and chatting...")
print("Question: Mô tả chi tiết tấm ảnh này\n")

response = client.chat_with_files(
    message="Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
    files=["71xUvQRYnvL._SY466_.webp"],
    model="qwen3-max",
    stream=True  # Enable streaming
)

print("\n" + "=" * 80)
print("📄 TEST: Chat with PDF (Streaming)")
print("=" * 80)

print("\n📤 Uploading and chatting...")
print("Question: Đây là đề thi gì?\n")

response2 = client.chat_with_files(
    message="Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
    files=["Đề N3 7-2015-13-15.pdf"],
    model="qwen3-max",
    stream=True
)

print("\n✅ Done!")
