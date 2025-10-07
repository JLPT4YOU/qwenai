#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test system prompt / instructions for Qwen API
"""

import requests
import json
import uuid
import time
import os

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjU0MjF9.kmOnOHqVpsm9nT1xwq3oWxbWTtOi9k9drbCnDOWeYDc")
BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

print("=" * 60)
print("  Testing System Prompt / Instructions")
print("=" * 60)

# Get chat ID
print("\n1. Getting chat ID...")
resp = requests.get(f"{BASE_URL}/v2/chats/?page=1", headers=headers)
chats = resp.json()
if not chats.get('data'):
    print("❌ No chats found")
    exit(1)

chat_id = chats['data'][0]['id']
print(f"✓ Using chat: {chat_id[:20]}...")

# Get parent_id from chat history
print("\n2. Getting parent_id from chat history...")
resp = requests.get(f"{BASE_URL}/v2/chats/{chat_id}", headers=headers)
chat_data = resp.json()
parent_id = chat_data.get('data', {}).get('currentId')
print(f"✓ Parent ID: {parent_id[:20] if parent_id else 'None'}...")

if not parent_id:
    parent_id = str(uuid.uuid4())

# Test different payload structures
test_cases = [
    {
        "name": "Method 1: System message in messages array",
        "payload": {
            "stream": False,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "role": "system",
                    "content": "Bạn là một trợ lý AI vui vẻ. Luôn trả lời ngắn gọn, không quá 2 câu."
                },
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "childrenIds": [],
                    "role": "user",
                    "content": "Giới thiệu về bạn",
                    "user_action": "chat",
                    "files": [],
                    "timestamp": int(time.time()),
                    "models": ["qwen3-max"],
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "extra": {
                        "meta": {
                            "subChatType": "t2t"
                        }
                    },
                    "sub_chat_type": "t2t",
                    "parent_id": parent_id
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Method 2: System prompt field",
        "payload": {
            "stream": False,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "system_prompt": "Bạn là một trợ lý AI vui vẻ. Luôn trả lời ngắn gọn.",
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "childrenIds": [],
                    "role": "user",
                    "content": "Giới thiệu về bạn",
                    "user_action": "chat",
                    "files": [],
                    "timestamp": int(time.time()),
                    "models": ["qwen3-max"],
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "extra": {
                        "meta": {
                            "subChatType": "t2t"
                        }
                    },
                    "sub_chat_type": "t2t",
                    "parent_id": parent_id
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Method 3: Instruction field",
        "payload": {
            "stream": False,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "instruction": "Bạn là một trợ lý AI vui vẻ. Luôn trả lời ngắn gọn.",
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "childrenIds": [],
                    "role": "user",
                    "content": "Giới thiệu về bạn",
                    "user_action": "chat",
                    "files": [],
                    "timestamp": int(time.time()),
                    "models": ["qwen3-max"],
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "extra": {
                        "meta": {
                            "subChatType": "t2t"
                        }
                    },
                    "sub_chat_type": "t2t",
                    "parent_id": parent_id
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Method 4: Inline in user message",
        "payload": {
            "stream": False,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "childrenIds": [],
                    "role": "user",
                    "content": "[INSTRUCTION: Bạn là một trợ lý AI vui vẻ. Luôn trả lời ngắn gọn, không quá 2 câu.]\n\nGiới thiệu về bạn",
                    "user_action": "chat",
                    "files": [],
                    "timestamp": int(time.time()),
                    "models": ["qwen3-max"],
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "extra": {
                        "meta": {
                            "subChatType": "t2t"
                        }
                    },
                    "sub_chat_type": "t2t",
                    "parent_id": parent_id
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    }
]

# Test each method
for i, test in enumerate(test_cases, 1):
    print(f"\n{i}. Testing: {test['name']}")
    print("-" * 60)
    
    try:
        resp = requests.post(
            f"{BASE_URL}/v2/chat/completions?chat_id={chat_id}",
            headers=headers,
            json=test['payload'],
            timeout=15
        )
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Try to extract response
            response_text = None
            if 'output' in data:
                response_text = data['output'].get('text', '')
            elif 'choices' in data and len(data['choices']) > 0:
                response_text = data['choices'][0].get('message', {}).get('content', '')
            elif 'content' in data:
                response_text = data.get('content', '')
            
            if response_text:
                print(f"✅ Success!")
                print(f"Response: {response_text[:150]}...")
            else:
                print(f"⚠️ Got 200 but no response text")
                print(f"Keys in response: {list(data.keys())}")
        else:
            print(f"❌ Failed: {resp.status_code}")
            try:
                error = resp.json()
                print(f"Error: {error}")
            except:
                print(f"Response: {resp.text[:200]}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n" + "=" * 60)
print("  Test Complete")
print("=" * 60)
