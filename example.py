"""
Example usage of Qwen AI Client
Demonstrates various features and use cases
"""

import os
from qwen_client import QwenClient


def example_quick_chat():
    """Example 1: Quick single message"""
    print("\n" + "="*50)
    print("Example 1: Quick Chat")
    print("="*50)
    
    client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
    
    print("\nSending: 'Hello, introduce yourself in one sentence'")
    print("\nResponse: ", end="")
    response = client.chat("Hello, introduce yourself in one sentence")
    print()


def example_conversation():
    """Example 2: Multi-turn conversation"""
    print("\n" + "="*50)
    print("Example 2: Multi-turn Conversation")
    print("="*50)
    
    client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
    
    # Create a conversation
    chat = client.create_chat()
    chat_id = chat["id"]
    print(f"\nCreated conversation: {chat_id[:16]}...\n")
    
    messages = [
        "My favorite color is blue",
        "What is my favorite color?",
        "Why is that color popular?"
    ]
    
    for msg in messages:
        print(f"\n→ You: {msg}")
        print("← AI: ", end="")
        client.send_message(chat_id, msg, stream=True)
        print()


def example_user_info():
    """Example 3: Get user information"""
    print("\n" + "="*50)
    print("Example 3: User Information")
    print("="*50)
    
    client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
    
    print("\nFetching user status...")
    try:
        status = client.get_user_status()
        print(f"✓ User Status: {status}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\nFetching user settings...")
    try:
        settings = client.get_user_settings()
        print(f"✓ User Settings: {settings}")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_list_chats():
    """Example 4: List recent conversations"""
    print("\n" + "="*50)
    print("Example 4: List Recent Chats")
    print("="*50)
    
    client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
    
    print("\nFetching chat list...")
    try:
        chats = client.list_chats(page=1)
        
        if chats.get("results"):
            print(f"\nFound {len(chats['results'])} conversations:")
            for i, chat in enumerate(chats["results"][:5], 1):
                chat_id = chat.get("id", "N/A")[:16]
                title = chat.get("title", "Untitled")
                print(f"  {i}. [{chat_id}...] {title}")
        else:
            print("No conversations found")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_non_streaming():
    """Example 5: Non-streaming response"""
    print("\n" + "="*50)
    print("Example 5: Non-streaming Response")
    print("="*50)
    
    client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
    
    # Create chat
    chat = client.create_chat()
    chat_id = chat["id"]
    
    print("\nSending message (non-streaming)...")
    print("→ You: Tell me a short joke\n")
    
    try:
        response = client.send_message(
            chat_id=chat_id,
            message="Tell me a short joke",
            stream=False
        )
        print(f"← AI: {response.get('content', response)}\n")
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all examples"""
    
    # Check for token
    if not os.getenv("QWEN_TOKEN"):
        print("❌ Error: QWEN_TOKEN environment variable not set")
        print("\nPlease set your token:")
        print("  export QWEN_TOKEN='your_token_here'")
        print("\nSee README.md for how to get your token")
        return
    
    print("\n" + "="*50)
    print("  QWEN AI CLIENT - EXAMPLES")
    print("="*50)
    print("\nThese examples demonstrate various features")
    print("of the Qwen AI Client.\n")
    
    try:
        # Run examples
        example_quick_chat()
        
        input("\nPress Enter to continue to next example...")
        example_conversation()
        
        input("\nPress Enter to continue to next example...")
        example_user_info()
        
        input("\nPress Enter to continue to next example...")
        example_list_chats()
        
        input("\nPress Enter to continue to next example...")
        example_non_streaming()
        
        print("\n" + "="*50)
        print("  All examples completed!")
        print("="*50)
        print("\nFor interactive chat, run: python chatbot.py")
        print("For documentation, see: README.md\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
