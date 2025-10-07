"""
Test /v1/auths/ endpoint
"""

import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjMzNjZ9.-S6huSievP_ddTRIPRoM0j8l2BN9ScEMZTgZnA9skik"
BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "source": "web"
}

print("=" * 60)
print("Testing /v1/auths/ endpoint")
print("=" * 60)

# Test GET
print("\n1. Testing GET /v1/auths/")
try:
    response = requests.get(f"{BASE_URL}/v1/auths/", headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response (text): {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test POST with empty body
print("\n2. Testing POST /v1/auths/ (empty)")
try:
    response = requests.post(f"{BASE_URL}/v1/auths/", headers=headers, json={}, timeout=10)
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response (text): {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test POST with model
print("\n3. Testing POST /v1/auths/ (with model)")
payloads = [
    {"model": "qwen3-max"},
    {"model_name": "qwen3-max"},
    {"chat_type": "t2t"},
    {"action": "create_chat"},
]

for payload in payloads:
    print(f"\nPayload: {payload}")
    try:
        response = requests.post(f"{BASE_URL}/v1/auths/", headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:300]}")
        except:
            print(f"Response (text): {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

# Test similar endpoints
print("\n" + "=" * 60)
print("Testing related endpoints")
print("=" * 60)

endpoints = [
    "/v1/auths",
    "/v2/auths/",
    "/v1/auth/",
    "/v2/auth/",
]

for endpoint in endpoints:
    print(f"\nGET {endpoint}")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                print(f"Response: {response.json()}")
            except:
                print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
