"""
Test the complete API flow with real message sending
"""

import requests
import json
import uuid
import time

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjAyODh9.n9pWIrTK6TCMyZSu0oSDs4XZR1mTmzaVHV9Z8G_AzIQ"
CHAT_ID = "5182b415-9927-49f9-8d73-00d98fde8a0e"
BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/event-stream",
    "x-accel-buffering": "no",
    "source": "web"
}

# Build payload
fid = str(uuid.uuid4())
parent_id = str(uuid.uuid4())
timestamp = int(time.time())

payload = {
    "stream": True,
    "incremental_output": True,
    "chat_id": CHAT_ID,
    "chat_mode": "normal",
    "model": "qwen3-max",
    "parent_id": parent_id,
    "messages": [
        {
            "fid": fid,
            "parentId": parent_id,
            "childrenIds": [],
            "role": "user",
            "content": "What is 5+3?",
            "user_action": "chat",
            "files": [],
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
        }
    ],
    "timestamp": timestamp
}

print("=" * 60)
print("Testing message send with streaming")
print("=" * 60)
print(f"\nPayload: {json.dumps(payload, indent=2)[:500]}...\n")

url = f"{BASE_URL}/v2/chat/completions?chat_id={CHAT_ID}"
print(f"URL: {url}\n")

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        stream=True,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}\n")
    
    if response.status_code == 200:
        print("Response (streaming):")
        print("-" * 60)
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                print(f"Raw: {line_str[:200]}")
                
                if line_str.startswith('data:'):
                    data_str = line_str[5:].strip()
                    if data_str and data_str != '[DONE]':
                        try:
                            data = json.loads(data_str)
                            print(f"Parsed: {json.dumps(data, indent=2)[:300]}")
                        except:
                            print(f"Could not parse: {data_str[:100]}")
        
        print("-" * 60)
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
