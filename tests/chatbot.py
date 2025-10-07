"""
Interactive Qwen AI Chatbot
Simple command-line interface for chatting with Qwen AI
"""

import os
import sys
from qwen_client import QwenClient


def interactive_chat():
    """Run interactive chat session"""
    
    # Get token from environment variable
    token = os.getenv("QWEN_TOKEN")
    
    if not token:
        print("Error: QWEN_TOKEN environment variable not set")
        print("\nTo set your token:")
        print("  export QWEN_TOKEN='your_token_here'")
        return
    
    client = QwenClient(auth_token=token)
    
    print("=" * 50)
    print("  Qwen AI Interactive Chatbot")
    print("=" * 50)
    print("\nCommands:")
    print("  - Type your message and press Enter to chat")
    print("  - Type 'exit' or 'quit' to end the session")
    print("  - Type 'new' to start a new conversation")
    print("  - Type 'help' to show this message again")
    print("\n" + "=" * 50 + "\n")
    
    # Create initial chat
    try:
        chat_data = client.create_chat()
        chat_id = chat_data.get("id")
        print(f"✓ New conversation started (ID: {chat_id[:8]}...)\n")
    except Exception as e:
        print(f"✗ Error creating chat: {e}")
        return
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye! 👋")
                break
            
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("  - Type your message to chat")
                print("  - 'exit' or 'quit' - End session")
                print("  - 'new' - Start new conversation")
                print("  - 'help' - Show this message\n")
                continue
            
            elif user_input.lower() == 'new':
                try:
                    chat_data = client.create_chat()
                    chat_id = chat_data.get("id")
                    print(f"\n✓ New conversation started (ID: {chat_id[:8]}...)\n")
                except Exception as e:
                    print(f"✗ Error creating new chat: {e}\n")
                continue
            
            # Send message and get response
            print("AI: ", end="", flush=True)
            try:
                response = client.send_message(chat_id, user_input, stream=True)
                print()  # Extra newline after response
            except Exception as e:
                print(f"\n✗ Error: {e}\n")
                # Try to create new chat if current one failed
                try:
                    chat_data = client.create_chat()
                    chat_id = chat_data.get("id")
                    print(f"✓ Created new conversation\n")
                except:
                    print("✗ Failed to recover. Please restart.\n")
                    break
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except EOFError:
            print("\n\nGoodbye! 👋")
            break


if __name__ == "__main__":
    interactive_chat()
