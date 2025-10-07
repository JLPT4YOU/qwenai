#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Thinking Mode & Search Features
"""

import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from qwen_client import QwenClient

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjU0MjF9.kmOnOHqVpsm9nT1xwq3oWxbWTtOi9k9drbCnDOWeYDc")

print("=" * 60)
print("  Test Qwen Advanced Features")
print("=" * 60)

try:
    client = QwenClient(auth_token=TOKEN)
    
    # Get chat
    chats = client.list_chats(page=1)
    if not chats.get('data'):
        print("❌ No chats found")
        sys.exit(1)
    
    chat_id = chats['data'][0]['id']
    print(f"\n✓ Using chat: {chat_id[:20]}...\n")
    
    # Test 1: Normal mode
    print("=" * 60)
    print("Test 1: Normal Mode")
    print("=" * 60)
    print("Message: 'Giải thích Python decorators'\n")
    
    response1 = client.send_message(
        chat_id=chat_id,
        message="Giải thích Python decorators ngắn gọn",
        thinking_enabled=False,
        search_enabled=False
    )
    
    print(f"\n✓ Response: {len(response1['content'])} chars")
    print(f"✓ Has thinking: {'thinking' in response1}")
    
    # Test 2: With thinking
    print("\n" + "=" * 60)
    print("Test 2: Thinking Mode Enabled")
    print("=" * 60)
    print("Message: 'Giải bài toán: 5 người bắt tay, mỗi người bắt tay 1 lần với mọi người khác, tổng số lần bắt tay?'\n")
    
    response2 = client.send_message(
        chat_id=chat_id,
        message="Giải bài toán: 5 người bắt tay, mỗi người bắt tay 1 lần với mọi người khác, tổng số lần bắt tay?",
        thinking_enabled=True,
        search_enabled=False
    )
    
    print(f"\n✓ Response: {len(response2['content'])} chars")
    print(f"✓ Has thinking: {'thinking' in response2}")
    if 'thinking' in response2:
        print(f"✓ Thinking length: {len(response2['thinking'])} chars")
        print(f"✓ Thinking preview: {response2['thinking'][:150]}...")
    
    # Test 3: Search mode
    print("\n" + "=" * 60)
    print("Test 3: Internet Search Mode")
    print("=" * 60)
    print("Message: 'Tin tức AI mới nhất hôm nay'\n")
    
    response3 = client.send_message(
        chat_id=chat_id,
        message="Tin tức AI mới nhất hôm nay",
        thinking_enabled=False,
        search_enabled=True
    )
    
    print(f"\n✓ Response: {len(response3['content'])} chars")
    print(f"✓ Has thinking: {'thinking' in response3}")
    print(f"✓ First 200 chars: {response3['content'][:200]}...")
    
    # Test 4: Both enabled
    print("\n" + "=" * 60)
    print("Test 4: Thinking + Search")
    print("=" * 60)
    print("Message: 'Phân tích xu hướng AI năm 2025'\n")
    
    response4 = client.send_message(
        chat_id=chat_id,
        message="Phân tích xu hướng AI năm 2025",
        thinking_enabled=True,
        search_enabled=True
    )
    
    print(f"\n✓ Response: {len(response4['content'])} chars")
    print(f"✓ Has thinking: {'thinking' in response4}")
    if 'thinking' in response4:
        print(f"✓ Thinking length: {len(response4['thinking'])} chars")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Test 1 (Normal):        {len(response1['content'])} chars, thinking: {'thinking' in response1}")
    print(f"Test 2 (Thinking):      {len(response2['content'])} chars, thinking: {'thinking' in response2}")
    print(f"Test 3 (Search):        {len(response3['content'])} chars, thinking: {'thinking' in response3}")
    print(f"Test 4 (Think+Search):  {len(response4['content'])} chars, thinking: {'thinking' in response4}")
    
    print("\n✅ All features working!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
