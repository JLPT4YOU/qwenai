"""
Test sending message to existing chat
"""

import requests
import json
import os

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjA4NjV9.OGJIlTgWdKoQmSjULCrEPGFQ7xoCu5ao7fFoPO33pyE")

BASE_URL = "https://chat.qwen.ai/api"
CHAT_ID = "5182b415-9927-49f9-8d73-00d98fde8a0e"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

print("\n" + "="*60)
print("Testing message sending endpoints")
print("="*60)

# Try different message endpoints
endpoints_to_try = [
    f"/v2/chats/{CHAT_ID}/messages",
    f"/v2/chats/{CHAT_ID}/message",
    f"/v1/chats/{CHAT_ID}/messages",
    f"/chats/{CHAT_ID}/messages",
]

message_payloads = [
    {
        "messages": [{"role": "user", "content": "test"}],
        "model": "qwen-max"
    },
    {
        "message": "test",
        "model": "qwen-max"
    },
    {
        "content": "test",
        "model_name": "qwen-max"
    },
]

for endpoint in endpoints_to_try:
    for payload in message_payloads:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTrying POST {endpoint}")
        print(f"Payload: {payload}")
        
        try:
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=10
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ SUCCESS!")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response (text): {response.text[:200]}")
                break
            else:
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response (text): {response.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")
    
print("\n" + "="*60)
