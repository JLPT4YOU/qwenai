#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Qwen Thinking Mode & Internet Search
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
    "User-Agent": "Mozilla/5.0",
    "source": "web"
}

print("=" * 60)
print("  Testing Qwen Thinking Mode & Features")
print("=" * 60)

# Get chat ID
print("\n1. Getting chat ID...")
resp = requests.get(f"{BASE_URL}/v2/chats/?page=1", headers=headers)
chats = resp.json()
if not chats.get('data'):
    print("❌ No chats found")
    exit(1)

chat_id = chats['data'][0]['id']
print(f"✓ Chat ID: {chat_id[:20]}...")

# Get parent_id
resp = requests.get(f"{BASE_URL}/v2/chats/{chat_id}", headers=headers)
chat_data = resp.json()
parent_id = chat_data.get('data', {}).get('currentId', str(uuid.uuid4()))
print(f"✓ Parent ID: {parent_id[:20]}...")

# Test cases
test_cases = [
    {
        "name": "Test 1: Normal Mode (t2t)",
        "payload": {
            "stream": True,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "role": "user",
                    "content": "2+2 bằng bao nhiêu?",
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "sub_chat_type": "t2t"
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Test 2: Thinking Mode Enabled",
        "payload": {
            "stream": True,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "role": "user",
                    "content": "Giải bài toán: Có 3 quả táo, tặng đi 1 quả, còn lại bao nhiêu?",
                    "chat_type": "t2t",
                    "feature_config": {
                        "thinking_enabled": True,  # ← Enable thinking
                        "output_schema": "phase"
                    },
                    "sub_chat_type": "t2t"
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Test 3: Search Mode (Internet)",
        "payload": {
            "stream": True,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "role": "user",
                    "content": "Tin tức mới nhất về AI hôm nay",
                    "chat_type": "search",  # ← Search mode
                    "feature_config": {
                        "thinking_enabled": False,
                        "output_schema": "phase"
                    },
                    "sub_chat_type": "search",
                    "extra": {
                        "meta": {
                            "subChatType": "search"
                        }
                    }
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    },
    {
        "name": "Test 4: Thinking + Search",
        "payload": {
            "stream": True,
            "incremental_output": False,
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": "qwen3-max",
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": str(uuid.uuid4()),
                    "parentId": parent_id,
                    "role": "user",
                    "content": "So sánh Python vs JavaScript, dựa trên xu hướng mới nhất",
                    "chat_type": "search",
                    "feature_config": {
                        "thinking_enabled": True,  # ← Both enabled
                        "output_schema": "phase"
                    },
                    "sub_chat_type": "search",
                    "extra": {
                        "meta": {
                            "subChatType": "search"
                        }
                    }
                }
            ],
            "timestamp": int(time.time()),
            "size": "1:1"
        }
    }
]

# Run tests
for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 60}")
    print(f"{i}. {test['name']}")
    print("=" * 60)
    
    try:
        resp = requests.post(
            f"{BASE_URL}/v2/chat/completions?chat_id={chat_id}",
            headers=headers,
            json=test['payload'],
            stream=True,
            timeout=30
        )
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print("\n📡 Streaming response:")
            print("-" * 60)
            
            # Parse SSE stream
            import sseclient
            client = sseclient.SSEClient(resp)
            
            full_response = ""
            thinking_content = ""
            has_thinking = False
            
            for event in client.events():
                if event.data == "[DONE]":
                    break
                
                try:
                    data = json.loads(event.data)
                    
                    # Check for thinking content
                    if "choices" in data and len(data["choices"]) > 0:
                        choice = data["choices"][0]
                        
                        # Regular content
                        if "delta" in choice:
                            content = choice["delta"].get("content", "")
                            reasoning = choice["delta"].get("reasoning_content", "")
                            
                            if reasoning:
                                thinking_content += reasoning
                                has_thinking = True
                            
                            if content:
                                full_response = content
                        
                        # Message format
                        elif "message" in choice:
                            msg = choice["message"]
                            content = msg.get("content", "")
                            reasoning = msg.get("reasoning_content", "")
                            
                            if reasoning:
                                thinking_content = reasoning
                                has_thinking = True
                            
                            if content:
                                full_response = content
                    
                    # Output format (alternative structure)
                    elif "output" in data:
                        content = data["output"].get("text", "")
                        reasoning = data["output"].get("reasoning", "")
                        
                        if reasoning:
                            thinking_content = reasoning
                            has_thinking = True
                        
                        if content:
                            full_response = content
                    
                except json.JSONDecodeError:
                    continue
            
            print("-" * 60)
            
            if has_thinking:
                print(f"\n💭 Thinking Content ({len(thinking_content)} chars):")
                print(thinking_content[:200] + "..." if len(thinking_content) > 200 else thinking_content)
            
            if full_response:
                print(f"\n💬 Response ({len(full_response)} chars):")
                print(full_response[:200] + "..." if len(full_response) > 200 else full_response)
            
            if not has_thinking and not full_response:
                print("⚠️ No content received")
        else:
            print(f"❌ Failed: {resp.status_code}")
            try:
                print(resp.json())
            except:
                print(resp.text[:200])
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
