#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Qwen Client - No chat_id needed!
"""

import os
import requests
from typing import Optional

class SimpleQwenClient:
    """
    Simplified Qwen client that auto-manages chat_id
    
    Usage:
        client = SimpleQwenClient(token)
        response = client.chat("Hello!")
        print(response)
    """
    
    def __init__(self, token: Optional[str] = None, api_base: str = "http://localhost:5001"):
        """
        Initialize client
        
        Args:
            token: Auth token (or set QWEN_TOKEN env var)
            api_base: API server URL
        """
        self.token = token or os.getenv("QWEN_TOKEN")
        if not self.token:
            raise ValueError("Token required! Set QWEN_TOKEN or pass token parameter")
        
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self,
        message: str,
        model: str = "qwen3-max",
        system_prompt: Optional[str] = None,
        thinking: bool = False,
        search: bool = False
    ) -> str:
        """
        Send message and get response - that's it!
        
        Args:
            message: Your message
            model: Model to use (default: qwen3-max)
            system_prompt: Optional instructions
            thinking: Enable thinking mode
            search: Enable internet search
            
        Returns:
            AI response as string
        """
        payload = {
            "message": message,
            "model": model
        }
        
        if system_prompt:
            payload["system_prompt"] = system_prompt
        if thinking:
            payload["thinking_enabled"] = True
        if search:
            payload["search_enabled"] = True
        
        response = requests.post(
            f"{self.api_base}/api/chat/quick",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            raise Exception(f"API error: {data.get('error', 'Unknown error')}")
        
        return data["data"]["content"]
    
    def models(self) -> list:
        """List available models"""
        response = requests.get(
            f"{self.api_base}/api/models",
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("data", [])]


# Convenience function for even simpler usage
def ask(message: str, **kwargs) -> str:
    """
    Ultra-simple one-liner
    
    Usage:
        from simple_client import ask
        
        print(ask("What is Python?"))
        print(ask("Write code", model="qwen3-coder"))
        print(ask("Latest news", search=True))
    """
    token = os.getenv("QWEN_TOKEN")
    if not token:
        raise ValueError("Set QWEN_TOKEN environment variable")
    
    client = SimpleQwenClient(token)
    return client.chat(message, **kwargs)


if __name__ == "__main__":
    import sys
    
    # Example usage
    print("=" * 60)
    print("  Simple Qwen Client - No chat_id needed!")
    print("=" * 60)
    
    try:
        client = SimpleQwenClient()
        
        # Test 1: Simple chat
        print("\n1. Simple chat:")
        response = client.chat("Hello! Introduce yourself in 1 sentence.")
        print(f"→ {response}\n")
        
        # Test 2: With system prompt
        print("2. With system prompt:")
        response = client.chat(
            "Giới thiệu Python",
            system_prompt="Trả lời ngắn gọn, tối đa 2 câu"
        )
        print(f"→ {response}\n")
        
        # Test 3: Coding model
        print("3. With coding model:")
        response = client.chat(
            "Write a hello world in Python",
            model="qwen3-coder"
        )
        print(f"→ {response}\n")
        
        # Test 4: List models
        print("4. Available models:")
        models = client.models()
        print(f"→ {len(models)} models: {', '.join(models[:5])}...\n")
        
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
