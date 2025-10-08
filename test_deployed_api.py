#!/usr/bin/env python3
"""Test deployed API on Vercel"""

import requests
import json
import sys

BASE_URL = "https://qwenai-two.vercel.app"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing /health endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_models(token):
    """Test models endpoint"""
    print("\n=== Testing /api/models endpoint ===")
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/models", headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available models: {len(data.get('models', []))} models")
        if data.get('models'):
            print(f"First model: {data['models'][0].get('name', 'N/A')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat(token):
    """Test chat endpoint"""
    print("\n=== Testing /api/chat/quick endpoint ===")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    payload = {
        "message": "Xin chào! Bạn là ai?",
        "model": "qwen-plus",
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/quick",
            headers=headers,
            json=payload,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                message = data['response']
                print(f"✅ Response: {message[:200]}...")
                return True
            else:
                print(f"Response: {data}")
                return False
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stream_chat(token):
    """Test streaming chat endpoint"""
    print("\n=== Testing /api/chat/quick with streaming ===")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    payload = {
        "message": "Đếm từ 1 đến 5",
        "model": "qwen-plus",
        "stream": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/quick",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Streaming response:")
            chunk_count = 0
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        chunk_count += 1
                        if chunk_count <= 3:  # Show first 3 chunks
                            print(f"  Chunk {chunk_count}: {line[:100]}...")
            print(f"Total chunks received: {chunk_count}")
            return chunk_count > 0
        else:
            print(f"❌ Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Testing Qwen API deployed on Vercel")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    # Get token from command line or prompt
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        print("\n⚠️  No token provided. Some tests may fail.")
        print("Usage: python test_deployed_api.py <qwen_token>")
        response = input("Continue without token? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Models List": test_models(token),
        "Chat (non-streaming)": test_chat(token),
        "Chat (streaming)": test_stream_chat(token)
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    main()
