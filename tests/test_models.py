#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Qwen Models API
"""

import requests
import json
import os

TOKEN = os.getenv("QWEN_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0NTA2Yjc4LWE3NjgtNGE1NS04OWFjLWM1ZmI2MWJlN2EwOCIsImxhc3RfcGFzc3dvcmRfY2hhbmdlIjoxNzU5ODE1NDY2LCJleHAiOjE3NjA0MjkwODN9.36PcMyiFED4yfB_tBPTZo9rjy3t2ylBZ2rKAbSaRdVg")
BASE_URL = "https://chat.qwen.ai/api"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "source": "web"
}

print("=" * 80)
print("  Qwen Models API Test")
print("=" * 80)

try:
    print("\n📡 Fetching models from API...")
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Save full response
        with open('/Users/nguyenbahoanglong/QWEN/models_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Full response saved to: models_response.json")
        
        # Parse and display models
        if isinstance(data, dict) and 'data' in data:
            models = data['data']
        elif isinstance(data, list):
            models = data
        else:
            models = [data]
        
        print(f"\n📊 Found {len(models)} models:")
        print("=" * 80)
        
        for i, model in enumerate(models, 1):
            if isinstance(model, dict):
                name = model.get('name', model.get('model', 'Unknown'))
                display_name = model.get('displayName', model.get('display_name', name))
                description = model.get('description', '')
                capabilities = model.get('capabilities', {})
                context_length = model.get('context_length', model.get('contextLength', 'N/A'))
                
                print(f"\n{i}. {display_name}")
                print(f"   ID: {name}")
                if description:
                    print(f"   Description: {description[:100]}...")
                print(f"   Context: {context_length} tokens")
                
                if capabilities:
                    caps = []
                    if capabilities.get('thinking'):
                        caps.append('💭 Thinking')
                    if capabilities.get('search'):
                        caps.append('🌐 Search')
                    if capabilities.get('vision'):
                        caps.append('👁️ Vision')
                    if capabilities.get('function_calling'):
                        caps.append('🔧 Function Calling')
                    
                    if caps:
                        print(f"   Capabilities: {', '.join(caps)}")
                
                print("-" * 80)
        
        # Find recommended models
        print("\n🎯 Recommended Models:")
        print("=" * 80)
        
        for model in models:
            if isinstance(model, dict):
                name = model.get('name', '')
                if 'max' in name.lower() or model.get('recommended'):
                    display = model.get('displayName', name)
                    print(f"✓ {display} ({name})")
        
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
