"""
Test script to discover Qwen API endpoints
"""

import requests
import json
import os

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjA4NjV9.OGJIlTgWdKoQmSjULCrEPGFQ7xoCu5ao7fFoPO33pyE")

BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def test_endpoint(method, endpoint, payload=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}")
        except:
            print(f"Response (text): {response.text[:500]}")
            
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test various endpoints
print("\n" + "="*60)
print("QWEN API ENDPOINT DISCOVERY")
print("="*60)

# GET endpoints
test_endpoint("GET", "/v2/users/status")
test_endpoint("GET", "/v2/chats?page=1")
test_endpoint("GET", "/config")

# Try creating chat with different approaches
test_endpoint("POST", "/v2/chats", {"model_name": "qwen-max"})
test_endpoint("POST", "/v2/chats/", {"model": "qwen-max"})
test_endpoint("POST", "/v1/chats", {"model": "qwen-max"})

# Try chat completions
test_endpoint("POST", "/chat/completions", {
    "model": "qwen-max",
    "messages": [{"role": "user", "content": "hi"}]
})

test_endpoint("POST", "/v1/chat/completions", {
    "model": "qwen-max", 
    "messages": [{"role": "user", "content": "hi"}]
})

print("\n" + "="*60)
print("DISCOVERY COMPLETE")
print("="*60)
