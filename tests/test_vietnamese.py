#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Vietnamese encoding
"""

import sys
import os

# Set UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from qwen_client import QwenClient

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjU0MjF9.kmOnOHqVpsm9nT1xwq3oWxbWTtOi9k9drbCnDOWeYDc")

print("=" * 60)
print("  Test Vietnamese Encoding")
print("=" * 60)

try:
    client = QwenClient(auth_token=TOKEN)
    
    # Get most recent chat
    chats = client.list_chats(page=1)
    if not chats.get('data'):
        print("❌ No chats found")
        sys.exit(1)
    
    chat_id = chats['data'][0]['id']
    print(f"\n✓ Using chat: {chat_id[:20]}...")
    
    # Test Vietnamese message
    print("\n📝 Sending Vietnamese message...")
    message = "Chào bạn! Hôm nay thế nào?"
    
    print(f"Message: {message}")
    print("\nResponse:")
    print("-" * 60)
    
    response = client.send_message(
        chat_id=chat_id,
        message=message,
        stream=True
    )
    
    print("-" * 60)
    print(f"\n✓ Response received: {len(response.get('content', ''))} characters")
    print(f"✓ First 100 chars: {response.get('content', '')[:100]}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
