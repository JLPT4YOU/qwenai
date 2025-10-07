"""
Qwen Official API Client using DashScope
This is the official and recommended way to use Qwen models
"""

import requests
import json
from typing import Optional, Dict, List, Generator
import sys


class QwenOfficialClient:
    """Client for Qwen Official API (DashScope)"""
    
    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    
    def __init__(self, api_key: str):
        """
        Initialize Qwen Official client
        
        Args:
            api_key: DashScope API key from https://dashscope.console.aliyun.com/
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })
    
    def chat(
        self, 
        message: str,
        model: str = "qwen-max",
        history: Optional[List[Dict]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        top_p: float = 0.8,
        max_tokens: int = 1500
    ) -> str:
        """
        Send a chat message
        
        Args:
            message: User message
            model: Model name (qwen-max, qwen-plus, qwen-turbo, etc.)
            history: Chat history as list of {"role": "user/assistant", "content": "..."}
            stream: Enable streaming
            temperature: Sampling temperature (0-2)
            top_p: Nucleus sampling parameter (0-1)
            max_tokens: Maximum tokens to generate
        
        Returns:
            AI response text
        """
        messages = history if history else []
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": temperature,
                "top_p": top_p,
                "max_tokens": max_tokens,
                "result_format": "message"
            }
        }
        
        if stream:
            payload["parameters"]["incremental_output"] = True
            return self._chat_stream(payload)
        else:
            return self._chat_sync(payload)
    
    def _chat_sync(self, payload: Dict) -> str:
        """Synchronous chat"""
        response = self.session.post(
            f"{self.BASE_URL}/services/aigc/text-generation/generation",
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get("output"):
            return result["output"]["choices"][0]["message"]["content"]
        
        raise Exception(f"API Error: {result}")
    
    def _chat_stream(self, payload: Dict) -> str:
        """Streaming chat"""
        response = self.session.post(
            f"{self.BASE_URL}/services/aigc/text-generation/generation",
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:])
                        if data.get("output"):
                            choices = data["output"].get("choices", [])
                            if choices:
                                content = choices[0]["message"]["content"]
                                if content:
                                    # Print incremental content
                                    if len(content) > len(full_response):
                                        new_content = content[len(full_response):]
                                        print(new_content, end="", flush=True)
                                    full_response = content
                    except json.JSONDecodeError:
                        continue
        
        print()  # New line
        return full_response
    
    def chat_multimodal(
        self,
        messages: List[Dict],
        model: str = "qwen-vl-max",
        stream: bool = True
    ) -> str:
        """
        Multimodal chat (text + images)
        
        Args:
            messages: List of messages with format:
                [
                    {
                        "role": "user",
                        "content": [
                            {"text": "What's in this image?"},
                            {"image": "https://example.com/image.jpg"}
                        ]
                    }
                ]
            model: Multimodal model name
            stream: Enable streaming
        
        Returns:
            AI response
        """
        payload = {
            "model": model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "result_format": "message"
            }
        }
        
        if stream:
            payload["parameters"]["incremental_output"] = True
            return self._chat_stream(payload)
        else:
            return self._chat_sync(payload)


def main():
    """Example usage"""
    import os
    
    api_key = os.getenv("DASHSCOPE_API_KEY")
    
    if not api_key:
        print("=" * 60)
        print("  Qwen Official API Client (DashScope)")
        print("=" * 60)
        print("\n❌ Error: DASHSCOPE_API_KEY not set")
        print("\n📝 To get your API key:")
        print("  1. Visit: https://dashscope.console.aliyun.com/")
        print("  2. Sign up / Login")
        print("  3. Go to API Keys section")
        print("  4. Create a new API key")
        print("\n🔧 Then set it:")
        print("  export DASHSCOPE_API_KEY='your_api_key_here'")
        print("\n" + "=" * 60)
        return
    
    client = QwenOfficialClient(api_key=api_key)
    
    print("=" * 60)
    print("  Qwen Official API Client")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        print(f"\nYou: {message}")
        print("AI: ", end="")
        try:
            response = client.chat(message, stream=True)
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            print("\nMake sure:")
            print("  1. Your API key is valid")
            print("  2. You have credits/quota in your account")
            print("  3. Network connection is stable")
    else:
        print("\nUsage: python qwen_official_client.py <your message>")
        print("Example: python qwen_official_client.py 'Hello, how are you?'")


if __name__ == "__main__":
    main()
