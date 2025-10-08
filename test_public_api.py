#!/usr/bin/env python3
"""Test public API endpoints (no token required)"""

import requests
import json

BASE_URL = "https://qwenai-two.vercel.app"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    return response.status_code == 200

def test_models():
    """Test models endpoint (should work with env token)"""
    print("\n🔍 Testing /api/models")
    response = requests.get(f"{BASE_URL}/api/models")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {len(data.get('models', []))} models")
        if data.get('models'):
            print(f"   First model: {data['models'][0].get('name')}")
    else:
        print(f"   ❌ Error: {response.text}")
    return response.status_code == 200

def test_token_info():
    """Test token info endpoint"""
    print("\n🔍 Testing /api/token/info")
    response = requests.get(f"{BASE_URL}/api/token/info")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Token source: {data.get('source')}")
        print(f"   Token length: {data.get('token_length')}")
    else:
        print(f"   ❌ Error: {response.text}")
    return response.status_code == 200

def test_quick_chat():
    """Test quick chat endpoint"""
    print("\n🔍 Testing /api/chat/quick")
    payload = {
        "message": "Xin chào! Hãy trả lời ngắn gọn.",
        "model": "qwen-plus"
    }
    response = requests.post(
        f"{BASE_URL}/api/chat/quick",
        json=payload,
        timeout=30
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            content = data.get('data', {}).get('content', '')
            print(f"   ✅ Response: {content[:100]}...")
        else:
            print(f"   Response: {data}")
    else:
        print(f"   ❌ Error: {response.text}")
    return response.status_code == 200

def main():
    print("=" * 60)
    print("Testing Qwen API (Public Endpoints)")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    results = {
        "Health Check": test_health(),
        "Models List": test_models(),
        "Token Info": test_token_info(),
        "Quick Chat": test_quick_chat()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n{passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
