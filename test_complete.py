"""Complete test: Create chat + Upload files + Chat"""
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTMxNTF9.XmnFBkUNi9xNPBLuEgP9DHxe6NPYRVETQyMAcdx5sl4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🎯 COMPLETE TEST: Create Chat + Upload + Chat with Files")
print("=" * 80)

# Test 1: Image
print("\n" + "=" * 80)
print("TEST 1: Image Analysis")
print("=" * 80)

print("\n1. Creating new chat...")
chat_data = client.create_chat(title="Image Analysis Test")
if chat_data and 'id' in chat_data:
    chat_id = chat_data['id']
    print(f"✓ Chat created: {chat_id}")
    
    print("\n2. Uploading image...")
    image_meta = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
    print(f"✓ Uploaded: {image_meta['name']}")
    
    print("\n3. Sending message with image...")
    print("Question: Mô tả tấm ảnh này\n")
    print("🤖 AI Response:")
    print("-" * 80)
    
    message_data = {
        "role": "user",
        "content": "Mô tả chi tiết tấm ảnh này. Đây là ảnh gì?",
        "files": [image_meta]
    }
    
    result = client.send_message(
        chat_id=chat_id,
        message=message_data,
        model="qwen3-max",
        stream=True
    )
    
    print("\n" + "-" * 80)
    print(f"✓ Response length: {len(result.get('content', ''))} chars")
else:
    print("❌ Failed to create chat")

# Test 2: PDF
print("\n" + "=" * 80)
print("TEST 2: PDF Analysis")
print("=" * 80)

print("\n1. Creating new chat...")
chat_data2 = client.create_chat(title="PDF Analysis Test")
if chat_data2 and 'id' in chat_data2:
    chat_id2 = chat_data2['id']
    print(f"✓ Chat created: {chat_id2}")
    
    print("\n2. Uploading PDF...")
    pdf_meta = client.upload_file("Đề N3 7-2015-13-15.pdf", filetype="file")
    print(f"✓ Uploaded: {pdf_meta['name']}")
    
    print("\n3. Sending message with PDF...")
    print("Question: Đây là đề thi gì?\n")
    print("🤖 AI Response:")
    print("-" * 80)
    
    message_data2 = {
        "role": "user",
        "content": "Đây là đề thi gì? Tóm tắt nội dung.",
        "files": [pdf_meta]
    }
    
    result2 = client.send_message(
        chat_id=chat_id2,
        message=message_data2,
        model="qwen3-max",
        stream=True
    )
    
    print("\n" + "-" * 80)
    print(f"✓ Response length: {len(result2.get('content', ''))} chars")
else:
    print("❌ Failed to create chat")

# Test 3: Both files
print("\n" + "=" * 80)
print("TEST 3: Both Files Together")
print("=" * 80)

print("\n1. Creating new chat...")
chat_data3 = client.create_chat(title="Multi-file Analysis")
if chat_data3 and 'id' in chat_data3:
    chat_id3 = chat_data3['id']
    print(f"✓ Chat created: {chat_id3}")
    
    print("\n2. Files already uploaded, reusing metadata...")
    
    print("\n3. Sending message with both files...")
    print("Question: Phân tích mối liên hệ\n")
    print("🤖 AI Response:")
    print("-" * 80)
    
    message_data3 = {
        "role": "user",
        "content": "Tôi có 2 file: 1 ảnh sách JLPT và 1 PDF đề thi. Chúng có liên quan gì đến nhau không?",
        "files": [image_meta, pdf_meta]
    }
    
    result3 = client.send_message(
        chat_id=chat_id3,
        message=message_data3,
        model="qwen3-max",
        stream=True
    )
    
    print("\n" + "-" * 80)
    print(f"✓ Response length: {len(result3.get('content', ''))} chars")
else:
    print("❌ Failed to create chat")

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED!")
print("=" * 80)
