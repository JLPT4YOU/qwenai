#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test system prompt functionality
"""

import sys
import os

# Set UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from qwen_client import QwenClient

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjU0MjF9.kmOnOHqVpsm9nT1xwq3oWxbWTtOi9k9drbCnDOWeYDc")

print("=" * 60)
print("  Test System Prompt Functionality")
print("=" * 60)

try:
    client = QwenClient(auth_token=TOKEN)
    
    # Get chat
    chats = client.list_chats(page=1)
    if not chats.get('data'):
        print("❌ No chats found")
        sys.exit(1)
    
    chat_id = chats['data'][0]['id']
    print(f"\n✓ Using chat: {chat_id[:20]}...")
    
    # Test 1: Without system prompt
    print("\n" + "=" * 60)
    print("Test 1: WITHOUT System Prompt")
    print("=" * 60)
    print("\n📝 Message: 'Giới thiệu về bạn'")
    print("\nResponse:")
    print("-" * 60)
    
    response1 = client.send_message(
        chat_id=chat_id,
        message="Giới thiệu về bạn",
        stream=True
    )
    
    print("-" * 60)
    print(f"Length: {len(response1.get('content', ''))} chars\n")
    
    # Test 2: With system prompt
    print("=" * 60)
    print("Test 2: WITH System Prompt")
    print("=" * 60)
    
    system_prompt = """Bạn là một trợ lý AI vui vẻ và thân thiện.
Quy tắc:
- Trả lời NGẮN GỌN, tối đa 2 câu
- Sử dụng emoji 😊
- Không giải thích dài dòng"""
    
    print(f"\n📋 System Prompt:\n{system_prompt}")
    print(f"\n📝 Message: 'Giới thiệu về bạn'")
    print("\nResponse:")
    print("-" * 60)
    
    response2 = client.send_message(
        chat_id=chat_id,
        message="Giới thiệu về bạn",
        system_prompt=system_prompt,
        stream=True
    )
    
    print("-" * 60)
    print(f"Length: {len(response2.get('content', ''))} chars\n")
    
    # Compare
    print("=" * 60)
    print("Comparison")
    print("=" * 60)
    print(f"Without system prompt: {len(response1.get('content', ''))} characters")
    print(f"With system prompt:    {len(response2.get('content', ''))} characters")
    
    if len(response2.get('content', '')) < len(response1.get('content', '')):
        print("\n✅ System prompt worked! Response is shorter as instructed.")
    else:
        print("\n⚠️ System prompt may not have full effect (but is prepended to message)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
