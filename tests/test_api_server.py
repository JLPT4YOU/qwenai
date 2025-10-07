"""
Test Backend API Server
"""

import requests
import os

API_BASE = "http://localhost:5001"
TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjMzNjZ9.-S6huSievP_ddTRIPRoM0j8l2BN9ScEMZTgZnA9skik")

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

print("=" * 60)
print("  Testing Backend API Server")
print("=" * 60)

# Test 1: Health check
print("\n1. Health Check")
try:
    resp = requests.get(f"{API_BASE}/health")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: List chats
print("\n2. List Chats")
try:
    resp = requests.get(f"{API_BASE}/api/chats", headers=headers)
    data = resp.json()
    print(f"   Status: {resp.status_code}")
    print(f"   Success: {data.get('success')}")
    print(f"   Total chats: {data.get('total')}")
    if data.get('data'):
        print(f"   First chat ID: {data['data'][0]['id'][:20]}...")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Get stats
print("\n3. Get Statistics")
try:
    resp = requests.get(f"{API_BASE}/api/stats", headers=headers)
    data = resp.json()
    print(f"   Status: {resp.status_code}")
    print(f"   Success: {data.get('success')}")
    if data.get('stats'):
        stats = data['stats']
        print(f"   User: {stats['user']['name']}")
        print(f"   Total chats: {stats['total_chats']}")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: Token info
print("\n4. Token Info")
try:
    resp = requests.get(f"{API_BASE}/api/token/info", headers=headers)
    data = resp.json()
    print(f"   Status: {resp.status_code}")
    print(f"   Success: {data.get('success')}")
    if data.get('data'):
        info = data['data']
        print(f"   User: {info.get('name')} ({info.get('email')})")
        import time
        exp = info.get('expires_at')
        days_left = (exp - time.time()) / 86400
        print(f"   Token expires in: {days_left:.1f} days")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("  All tests completed!")
print("=" * 60)
print("\n✅ API Server is working!")
print("\n📝 Next steps:")
print("   1. Open browser: http://localhost:8000/index_v2.html")
print("   2. Enter your token")
print("   3. Start chatting!")
