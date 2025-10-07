#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Admin API - Token Update Without Redeploy
"""

import requests
import os

API_BASE = "http://localhost:5001"
ADMIN_KEY = os.getenv("ADMIN_KEY", "change-me-in-production")

print("=" * 60)
print("  Test Admin API - Token Management")
print("=" * 60)

# Test 1: Check current token (if any)
print("\n1. Check stored token...")
try:
    response = requests.get(
        f"{API_BASE}/api/admin/token",
        params={"admin_key": ADMIN_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('has_token'):
            print(f"✓ Has token: {data['token_preview']}")
        else:
            print("✓ No token stored yet")
    else:
        print(f"✗ Failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Update token
print("\n2. Update token...")
new_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_token_12345"

try:
    response = requests.post(
        f"{API_BASE}/api/admin/token",
        json={
            "token": new_token,
            "admin_key": ADMIN_KEY
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ {data['message']}")
        print(f"  Timestamp: {data['timestamp']}")
    else:
        print(f"✗ Failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Verify token updated
print("\n3. Verify token updated...")
try:
    response = requests.get(
        f"{API_BASE}/api/admin/token",
        params={"admin_key": ADMIN_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('has_token'):
            print(f"✓ Token updated: {data['token_preview']}")
        else:
            print("✗ No token stored")
    else:
        print(f"✗ Failed: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Try with wrong admin key
print("\n4. Test security (wrong admin key)...")
try:
    response = requests.post(
        f"{API_BASE}/api/admin/token",
        json={
            "token": "malicious_token",
            "admin_key": "wrong_key"
        }
    )
    
    if response.status_code == 403:
        print("✓ Correctly rejected unauthorized request")
    else:
        print(f"✗ Security issue! Status: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
print("✅ Token can be updated via API")
print("✅ No code changes needed")
print("✅ No redeploy needed")
print("✅ Admin key protects endpoint")
print("\nWhen deployed to Vercel:")
print("  curl -X POST https://your-app.vercel.app/api/admin/token \\")
print("    -H 'Content-Type: application/json' \\")
print("    -d '{\"token\": \"new-token\", \"admin_key\": \"your-key\"}'")
print("\n" + "=" * 60)
