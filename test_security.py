#!/usr/bin/env python3
"""Test API security features"""

import requests

BASE_URL = "https://qwenai-two.vercel.app"

def test_without_origin():
    """Test request without Origin header (should work from curl)"""
    print("\n🔍 Test 1: Request without Origin header")
    response = requests.get(f"{BASE_URL}/api/models")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Passed - Works without Origin")
    else:
        print(f"   Response: {response.json()}")

def test_with_valid_origin():
    """Test with valid origin"""
    print("\n🔍 Test 2: Request with valid origin (jlpt4you.com)")
    headers = {"Origin": "https://jlpt4you.com"}
    response = requests.get(f"{BASE_URL}/api/models", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Passed - Valid origin accepted")
    else:
        print(f"   Response: {response.json()}")

def test_with_invalid_origin():
    """Test with invalid origin"""
    print("\n🔍 Test 3: Request with invalid origin (example.com)")
    headers = {"Origin": "https://example.com"}
    response = requests.get(f"{BASE_URL}/api/models", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 403:
        print("   ✅ Passed - Invalid origin blocked")
        print(f"   Error: {response.json().get('error')}")
    else:
        print(f"   ❌ Failed - Should be blocked but got: {response.status_code}")

def test_environment_check():
    """Test environment restriction"""
    print("\n🔍 Test 4: Environment check")
    response = requests.get(f"{BASE_URL}/api/models")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 403:
        data = response.json()
        if "development environment" in data.get('error', ''):
            print("   ⚠️  ENVIRONMENT is set to 'production'")
            print("   ℹ️  Set ENVIRONMENT=development in Vercel to enable API")
        else:
            print(f"   Response: {data}")
    elif response.status_code == 200:
        print("   ✅ Environment is 'development' - API is accessible")
    else:
        print(f"   Response: {response.json()}")

def test_health_endpoint():
    """Test health endpoint (should always work)"""
    print("\n🔍 Test 5: Health endpoint (no security)")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Passed - Health endpoint accessible")
    else:
        print(f"   ❌ Failed: {response.text}")

def main():
    print("=" * 60)
    print("Testing API Security Features")
    print(f"Base URL: {BASE_URL}")
    print("=" * 60)
    
    test_health_endpoint()
    test_environment_check()
    test_without_origin()
    test_with_valid_origin()
    test_with_invalid_origin()
    
    print("\n" + "=" * 60)
    print("IMPORTANT NOTES:")
    print("=" * 60)
    print("1. Đảm bảo ENVIRONMENT=development trong Vercel env vars")
    print("2. API chỉ chấp nhận requests từ jlpt4you.com và localhost")
    print("3. Health endpoint (/health) không có security check")
    print("=" * 60)

if __name__ == "__main__":
    main()
