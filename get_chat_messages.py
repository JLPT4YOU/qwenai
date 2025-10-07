"""
Get messages from a chat to find parent_id
"""

import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjAyODh9.n9pWIrTK6TCMyZSu0oSDs4XZR1mTmzaVHV9Z8G_AzIQ"
CHAT_ID = "5182b415-9927-49f9-8d73-00d98fde8a0e"
BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Try getting chat details
url = f"{BASE_URL}/v2/chats/{CHAT_ID}"
print(f"Getting chat details from: {url}\n")

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.text}")
