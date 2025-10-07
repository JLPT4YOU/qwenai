"""
Test token refresh functionality
"""

from qwen_client import QwenClient
import os

# Use token from environment
token = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjMzNjZ9.-S6huSievP_ddTRIPRoM0j8l2BN9ScEMZTgZnA9skik")

print("=" * 60)
print("  Qwen Token Refresh Test")
print("=" * 60)

client = QwenClient(auth_token=token)

print("\n1. Get current token info:")
try:
    info = client.get_token_info()
    print(f"   User: {info.get('name')} ({info.get('email')})")
    print(f"   User ID: {info.get('id')}")
    print(f"   Current Token: {info.get('token')[:50]}...")
    
    import time
    expires_at = info.get('expires_at')
    if expires_at:
        exp_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expires_at))
        days_left = (expires_at - time.time()) / (24 * 3600)
        print(f"   Expires at: {exp_date}")
        print(f"   Days remaining: {days_left:.1f} days")
    
    print(f"   Permissions:")
    perms = info.get('permissions', {})
    for category, settings in perms.items():
        print(f"     - {category}: {settings}")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Refresh token:")
try:
    new_info = client.refresh_token()
    print(f"   New Token: {new_info.get('token')[:50]}...")
    print(f"   Token refreshed successfully!")
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Test with refreshed token:")
try:
    status = client.get_user_status()
    print(f"   ✓ User status check: {status}")
    
    chats = client.list_chats(page=1)
    chat_count = len(chats.get('data', []))
    print(f"   ✓ Found {chat_count} chats")
    
    if chat_count > 0:
        print(f"   ✓ Token is working correctly!")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("  Token refresh test completed!")
print("=" * 60)
