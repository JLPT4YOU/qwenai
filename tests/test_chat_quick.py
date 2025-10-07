"""
Test quick chat endpoint
"""

import requests

API_BASE = "http://localhost:5001"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjMzNjZ9.-S6huSievP_ddTRIPRoM0j8l2BN9ScEMZTgZnA9skik"

print("Testing quick chat endpoint...")
print("=" * 60)

try:
    response = requests.post(
        f"{API_BASE}/api/chat/quick",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "message": "Say hello in Vietnamese"
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data.get("success"):
        print("✅ Success!")
        print(f"Chat ID: {data.get('chat_id', 'N/A')}")
        print(f"Response: {data['data']['content'][:200]}...")
    else:
        print("❌ Failed!")
        print(f"Error: {data.get('error')}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 60)
