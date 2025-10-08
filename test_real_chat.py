"""Test with real existing chat"""
from qwen_client import QwenClient

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

client = QwenClient(auth_token=token)

print("=" * 80)
print("🔍 Getting existing chats...")
print("=" * 80)

# Get list of chats
chats = client.list_chats(page=1)
if chats.get('success') and chats.get('data'):
    chat_list = chats['data']
    if len(chat_list) > 0:
        # Use first chat
        existing_chat = chat_list[0]
        chat_id = existing_chat['id']
        print(f"\n✓ Found chat: {existing_chat.get('title', 'Untitled')}")
        print(f"  Chat ID: {chat_id}")
        
        # Upload file
        print("\n📤 Uploading image...")
        image_meta = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
        print(f"✓ Uploaded: {image_meta['name']}")
        
        # Send message to existing chat
        print(f"\n💬 Sending message to existing chat...")
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
        print(f"\nResult: {result}")
    else:
        print("\n⚠️  No chats found")
else:
    print(f"\n❌ Failed to get chats: {chats}")

print("\n✅ Done!")
