"""Simplest test using chat() method"""
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🖼️  TEST: Image Analysis")
print("=" * 80)

print("\n📤 Uploading and analyzing image...")
print("File: 71xUvQRYnvL._SY466_.webp")
print("Question: Mô tả chi tiết tấm ảnh này\n")

print("🤖 AI Response:")
print("-" * 80)

# Use chat_with_files which handles everything
response = client.chat_with_files(
    message="Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
    files=["71xUvQRYnvL._SY466_.webp"],
    model="qwen3-max",
    stream=True  # This should print to console
)

print("\n" + "-" * 80)
print(f"Response type: {type(response)}")
if isinstance(response, dict):
    print(f"Content: {response.get('content', 'NO CONTENT')[:200]}")

print("\n" + "=" * 80)
print("📄 TEST: PDF Analysis")
print("=" * 80)

print("\n📤 Uploading and analyzing PDF...")
print("File: Đề N3 7-2015-13-15.pdf")
print("Question: Đây là đề thi gì?\n")

print("🤖 AI Response:")
print("-" * 80)

response2 = client.chat_with_files(
    message="Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
    files=["Đề N3 7-2015-13-15.pdf"],
    model="qwen3-max",
    stream=True
)

print("\n" + "-" * 80)
if isinstance(response2, dict):
    print(f"Content: {response2.get('content', 'NO CONTENT')[:200]}")

print("\n✅ Done!")
