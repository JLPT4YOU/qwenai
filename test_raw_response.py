"""Test raw API response"""
import requests
import json
import uuid
import time

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0OTAxNDd9.hvFr4KoSOfo7s7ZyoGZztWw1dBq7euWcqesNLmTlzH4"

# First upload file
from qwen_client import QwenClient
client = QwenClient(auth_token=token)

print("1. Uploading file...")
file_metadata = client.upload_file("71xUvQRYnvL._SY466_.webp", filetype="image")
print(f"✓ File ID: {file_metadata['id']}")

# Prepare request
chat_id = str(uuid.uuid4())
fid = str(uuid.uuid4())
parent_id = str(uuid.uuid4())
timestamp = int(time.time())

payload = {
    "stream": False,  # Non-streaming first
    "incremental_output": False,
    "chat_id": chat_id,
    "chat_mode": "normal",
    "model": "qwen3-max",
    "parent_id": parent_id,
    "messages": [{
        "fid": fid,
        "parentId": parent_id,
        "childrenIds": [],
        "role": "user",
        "content": "Mô tả tấm ảnh này",
        "user_action": "chat",
        "files": [file_metadata],
        "timestamp": timestamp,
        "models": ["qwen3-max"],
        "chat_type": "t2t",
        "feature_config": {
            "thinking_enabled": False,
            "output_schema": "phase"
        },
        "extra": {
            "meta": {
                "subChatType": "t2t"
            }
        },
        "sub_chat_type": "t2t",
        "parent_id": parent_id
    }],
    "timestamp": timestamp
}

print("\n2. Sending request...")
print(f"Chat ID: {chat_id}")
print(f"Files: {len(payload['messages'][0]['files'])}")

response = requests.post(
    f"https://chat.qwen.ai/api/v2/chat/completions?chat_id={chat_id}",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    },
    json=payload
)

print(f"\n3. Response status: {response.status_code}")
print(f"Response headers: {dict(response.headers)}")

if response.status_code == 200:
    try:
        data = response.json()
        print(f"\n4. Response JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"\n4. Response text:")
        print(response.text[:1000])
else:
    print(f"\nError: {response.text}")
