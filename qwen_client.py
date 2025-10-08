"""Qwen AI Chat Client
Unofficial Python client for interacting with Qwen AI Chat API
"""

import requests
import json
import os
from typing import Optional, Dict, List
import sseclient
import sys
import uuid
import time


class QwenClient:
    """Client for interacting with Qwen AI Chat API"""
    
    # Get base URL from environment or use default
    BASE_URL = os.getenv("QWEN_API_URL", "https://chat.qwen.ai/api")
    
    def __init__(self, auth_token: str, auto_refresh: bool = True, base_url: Optional[str] = None):
        """
        Initialize Qwen client
        
        Args:
            auth_token: JWT authentication token from Qwen
            auto_refresh: Automatically refresh token when needed
            base_url: Custom base URL (overrides environment variable)
        """
        self.auth_token = auth_token
        self.auto_refresh = auto_refresh
        
        # Allow custom base URL or use class default (from env)
        if base_url:
            self.BASE_URL = base_url
        
        self.session = requests.Session()
        self._update_session_headers()
    
    def _update_session_headers(self):
        """Update session headers with current token"""
        self.session.headers.update({
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
    
    def get_user_settings(self) -> Dict:
        """Get user settings"""
        response = self.session.get(f"{self.BASE_URL}/v2/users/user/settings")
        response.raise_for_status()
        return response.json()
    
    def refresh_token(self) -> Dict:
        """
        Refresh authentication token
        
        Returns:
            Dict with new token info including expires_at
        """
        response = self.session.get(f"{self.BASE_URL}/v1/auths/")
        response.raise_for_status()
        data = response.json()
        
        # Update token
        if 'token' in data:
            self.auth_token = data['token']
            self._update_session_headers()
            print(f"✓ Token refreshed. Expires at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['expires_at']))}")
        
        return data
    
    def get_token_info(self) -> Dict:
        """
        Get current user and token information
        
        Returns:
            Dict with user info, token, and expiration
        """
        response = self.session.get(f"{self.BASE_URL}/v1/auths/")
        response.raise_for_status()
        return response.json()
    
    def get_user_status(self) -> Dict:
        """Get user status"""
        response = self.session.get(f"{self.BASE_URL}/v2/users/status")
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> Dict:
        """
        List available models with their capabilities
        
        Returns:
            Dict with models list and their info
        """
        response = self.session.get(f"{self.BASE_URL}/models")
        response.raise_for_status()
        return response.json()
    
    def list_chats(self, page: int = 1) -> Dict:
        """
        List all chat conversations
        
        Args:
            page: Page number for pagination
        """
        response = self.session.get(f"{self.BASE_URL}/v2/chats/?page={page}")
        response.raise_for_status()
        return response.json()
    
        """Get pinned chat conversations"""
        response = self.session.get(f"{self.BASE_URL}/v2/chats/pinned")
        response.raise_for_status()
        return response.json()
    
    def create_chat(self, title: str = "New Chat", model: str = "qwen3-max") -> Dict:
        """
        Create a new chat conversation
        
        Args:
            title: Chat title
            model: Model to use
        
        Returns:
            Dict with chat info including 'id'
        """
        try:
            import time
            payload = {
                "title": title,
                "models": [model],
                "chat_mode": "normal",
                "chat_type": "t2t",
                "timestamp": int(time.time() * 1000)  # milliseconds
            }
            response = self.session.post(
                f"{self.BASE_URL}/v2/chats/new",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Check if success
            if result.get("success") and result.get("data"):
                return result["data"]
            
            return result
            
        except Exception as e:
            raise
    
    def send_message(
        self,
        chat_id: str,
        message,  # Can be str or dict with files
        model: str = "qwen3-max",
        parent_id: Optional[str] = None,
        stream: bool = True,
        system_prompt: Optional[str] = None,
        thinking_enabled: bool = False,
        search_enabled: bool = False
    ) -> Dict:
        """
        Send a message to a chat conversation
        
        Args:
            chat_id: Chat conversation ID
            message: Message content (str) or message dict with files
            model: Model name (qwen3-max, qwen-plus, qwen-turbo)
            parent_id: Parent message ID for conversation threading (auto-detected if None)
            stream: Enable streaming response
            system_prompt: Optional system instruction/prompt to prepend to message
            thinking_enabled: Enable thinking mode (shows reasoning process)
            search_enabled: Enable internet search mode (gets latest information)
        """
        
        # Handle message as dict (with files) or string
        if isinstance(message, dict):
            message_content = message.get('content', '')
            files = message.get('files', [])
        else:
            message_content = message
            files = []
        
        # Prepend system prompt if provided
        if system_prompt:
            message_content = f"""[INSTRUCTION]
{system_prompt}

[MESSAGE]
{message_content}
"""
        # Auto-detect parent_id from chat history if not provided
        if parent_id is None:
            try:
                chat_data = self.get_chat_history(chat_id)
                if chat_data.get("success") and chat_data.get("data"):
                    parent_id = chat_data["data"].get("currentId")
            except:
                # For new chats, parent_id should be null
                pass
        
        # Generate IDs
        fid = str(uuid.uuid4())
        
        timestamp = int(time.time())
        
        # Determine chat type based on search mode
        chat_type = "search" if search_enabled else "t2t"
        sub_chat_type = "search" if search_enabled else "t2t"
        
        # Build payload matching Qwen's format
        payload = {
            "stream": stream,
            "incremental_output": True,  # True for streaming output
            "chat_id": chat_id,
            "chat_mode": "normal",
            "model": model,
            "parent_id": parent_id,
            "messages": [
                {
                    "fid": fid,
                    "parentId": parent_id,
                    "childrenIds": [],
                    "role": "user",
                    "content": message_content,
                    "user_action": "chat",
                    "files": files,  # Include files here
                    "timestamp": timestamp,
                    "models": [model],
                    "chat_type": chat_type,
                    "feature_config": {
                        "thinking_enabled": thinking_enabled,  # Enable/disable thinking
                        "output_schema": "phase"
                    },
                    "extra": {
                        "meta": {
                            "subChatType": sub_chat_type
                        }
                    },
                    "sub_chat_type": sub_chat_type,
                    "parent_id": parent_id
                }
            ],
            "timestamp": timestamp,
            "size": "1:1"
        }
        
        if stream:
            return self._send_message_stream(chat_id, payload)
        else:
            response = self.session.post(
                f"{self.BASE_URL}/v2/chat/completions?chat_id={chat_id}",
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    def _send_message_stream(self, chat_id: str, payload: Dict):
        """Handle streaming response"""
        # Add headers for streaming
        headers = self.session.headers.copy()
        headers.update({
            "Accept": "text/event-stream",
            "x-accel-buffering": "no",
            "source": "web"
        })
        
        response = self.session.post(
            f"{self.BASE_URL}/v2/chat/completions?chat_id={chat_id}",
            json=payload,
            stream=True,
            headers=headers
        )
        response.raise_for_status()
        
        # Ensure UTF-8 encoding
        response.encoding = 'utf-8'
        
        client = sseclient.SSEClient(response)
        full_response = ""
        thinking_content = ""
        last_printed_length = 0
        last_thinking_length = 0
        
        for event in client.events():
            if event.data == "[DONE]":
                break
            try:
                # Properly decode JSON with UTF-8
                data = json.loads(event.data, strict=False)
                
                # Qwen format: check for content in different structures
                content = None
                reasoning = None
                
                if "output" in data:
                    content = data["output"].get("text", "")
                    reasoning = data["output"].get("reasoning", "")
                elif "choices" in data and len(data["choices"]) > 0:
                    choice = data["choices"][0]
                    
                    # Delta format (streaming)
                    if "delta" in choice:
                        delta = choice["delta"]
                        content = delta.get("content", "")
                        reasoning = delta.get("reasoning_content", "")
                    
                    # Message format (final)
                    elif "message" in choice:
                        msg = choice["message"]
                        content = msg.get("content", "")
                        reasoning = msg.get("reasoning_content", "")
                
                elif "content" in data:
                    content = data.get("content", "")
                    reasoning = data.get("reasoning_content", "")
                
                # Handle thinking/reasoning content
                if reasoning:
                    if isinstance(reasoning, bytes):
                        reasoning = reasoning.decode('utf-8', errors='replace')
                    
                    thinking_content = reasoning
                    
                    # Print thinking content (in different color if possible)
                    if len(thinking_content) > last_thinking_length:
                        new_thinking = thinking_content[last_thinking_length:]
                        print(f"\n💭 [Thinking: {new_thinking[:100]}...]", end="", flush=True)
                        last_thinking_length = len(thinking_content)
                
                # Handle regular content
                if content:
                    # Ensure content is properly decoded UTF-8
                    if isinstance(content, bytes):
                        content = content.decode('utf-8', errors='replace')
                    
                    # With incremental_output=True, each event contains only new content
                    full_response += content
                    
                    # Print the new content directly
                    print(content, end="", flush=True)
                        
            except json.JSONDecodeError:
                continue
            except Exception as e:
                # Log but continue
                print(f"\n[Parse error: {e}]", end="", flush=True)
                continue
        
        print()  # New line after streaming
        
        result = {"content": full_response}
        if thinking_content:
            result["thinking"] = thinking_content
        
        return result
    
    def get_chat_history(self, chat_id: str) -> Dict:
        """
        Get chat conversation history
        
        Args:
            chat_id: Chat conversation ID
        """
        response = self.session.get(f"{self.BASE_URL}/v2/chats/{chat_id}")
        response.raise_for_status()
        return response.json()
    
    def delete_chat(self, chat_id: str) -> bool:
        """
        Delete a chat conversation
        
        Args:
            chat_id: Chat conversation ID
        """
        response = self.session.delete(f"{self.BASE_URL}/v2/chats/{chat_id}")
        response.raise_for_status()
        return True
    
    def chat(self, message: str, model: str = "qwen3-max", chat_id: Optional[str] = None) -> str:
        """
        Quick chat - sends message to existing or new chat
        
        Args:
            message: Message to send
            model: Model name (qwen-max, qwen3-max, qwen-plus, qwen-turbo)
            chat_id: Optional existing chat ID. If None, lists chats to find one or asks user
        
        Returns:
            AI response text
        """
        try:
            # If no chat_id provided, try to get from existing chats
            if not chat_id:
                chats = self.list_chats(page=1)
                if chats.get("success") and chats.get("data") and len(chats["data"]) > 0:
                    # Use the most recent chat
                    chat_id = chats["data"][0]["id"]
                    print(f"Using existing chat: {chat_id[:16]}...")
                else:
                    print("No existing chats found. Please create a chat on web first or provide chat_id.")
                    print("Visit https://chat.qwen.ai to create a new chat, then run:")
                    print("  python qwen_client.py --list-chats")
                    return ""
            
            # Send message
            response = self.send_message(chat_id, message, model=model, stream=True)
            return response.get("content", "")
            
        except Exception as e:
            print(f"\nError: {e}")
            raise
    
    def get_sts_token(self, filename: str, filesize: int, filetype: str = "image") -> Dict:
        """
        Get STS token for uploading file to OSS
        
        Args:
            filename: Name of the file
            filesize: Size of the file in bytes
            filetype: Type of file ("image" or "file")
        
        Returns:
            Dict with STS credentials and upload info
        """
        response = self.session.post(
            f"{self.BASE_URL}/v2/files/getstsToken",
            json={
                "filename": filename,
                "filesize": filesize,
                "filetype": filetype
            }
        )
        response.raise_for_status()
        return response.json()
    
    def upload_file_to_oss(self, file_path: str, sts_data: Dict) -> str:
        """
        Upload file to Alibaba OSS using STS credentials
        
        Args:
            file_path: Path to the file to upload
            sts_data: STS token data from get_sts_token()
        
        Returns:
            URL of the uploaded file
        """
        try:
            import oss2
            from oss2 import StsAuth
        except ImportError:
            raise ImportError("oss2 package required. Install with: pip install oss2")
        
        # Create auth with STS credentials
        auth = StsAuth(
            sts_data['access_key_id'],
            sts_data['access_key_secret'],
            sts_data['security_token']
        )
        
        # Create bucket instance
        endpoint = f"https://{sts_data['endpoint']}"
        bucket = oss2.Bucket(auth, endpoint, sts_data['bucketname'])
        
        # Upload file
        with open(file_path, 'rb') as f:
            bucket.put_object(sts_data['file_path'], f)
        
        # Return the file URL (use pre-signed URL from response)
        file_url = sts_data.get('file_url', f"https://{sts_data['bucketname']}.{sts_data['endpoint']}/{sts_data['file_path']}")
        return file_url
    
    def upload_file(self, file_path: str, filetype: str = None) -> Dict:
        """
        Complete file upload flow: get STS token, upload to OSS, return metadata
        
        Args:
            file_path: Path to the file to upload
            filetype: Type of file ("image" or "file"). Auto-detected if None.
        
        Returns:
            Dict with file metadata ready to use in messages
        """
        from pathlib import Path
        import mimetypes
        
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Get file info
        filename = file_path_obj.name
        filesize = file_path_obj.stat().st_size
        
        # Auto-detect filetype if not provided
        if filetype is None:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('image/'):
                filetype = "image"
            else:
                filetype = "file"
        
        # Get STS token
        sts_response = self.get_sts_token(filename, filesize, filetype)
        
        # Extract data from response
        if sts_response.get('success'):
            sts_data = sts_response['data']
        else:
            raise Exception(f"Failed to get STS token: {sts_response}")
        
        # Upload to OSS
        file_url = self.upload_file_to_oss(file_path, sts_data)
        
        # Prepare file metadata
        mime_type, _ = mimetypes.guess_type(file_path)
        file_class = "vision" if filetype == "image" else "document"
        
        return {
            "type": filetype,
            "id": sts_data['file_id'],
            "url": file_url,
            "name": filename,
            "size": filesize,
            "file_type": mime_type or "application/octet-stream",
            "file_class": file_class,
            "status": "uploaded"
        }
    
    def chat_with_files(
        self,
        message: str,
        files: List[str] = None,
        chat_id: Optional[str] = None,
        model: str = "qwen3-max",
        stream: bool = True,
        thinking_enabled: bool = False
    ) -> str:
        """
        Send a chat message with file attachments
        
        Args:
            message: The message text
            files: List of file paths to upload and attach
            chat_id: Existing chat ID or None for new chat
            model: Model to use
            stream: Whether to stream the response
            thinking_enabled: Enable thinking mode
        
        Returns:
            The AI's response text
        """
        # Upload files if provided
        file_metadata = []
        if files:
            for file_path in files:
                print(f"Uploading {file_path}...")
                metadata = self.upload_file(file_path)
                file_metadata.append(metadata)
                print(f"✓ Uploaded: {metadata['name']}")
        
        # Create or use existing chat
        if not chat_id:
            chat_id = str(uuid.uuid4())
        
        # Prepare message with files
        message_data = {
            "role": "user",
            "content": message,
            "files": file_metadata
        }
        
        # Send message
        return self.send_message(
            chat_id=chat_id,
            message=message_data,
            model=model,
            stream=stream,
            thinking_enabled=thinking_enabled
        )


def main():
    """Example usage"""
    import os
    
    # Get token from environment
    token = os.getenv("QWEN_TOKEN")
    
    if not token:
        print("=" * 60)
        print("  Qwen AI Chat Client")
        print("=" * 60)
        print("\n❌ Error: QWEN_TOKEN not set")
        print("\nTo get your token:")
        print("  1. Visit https://chat.qwen.ai and login")
        print("  2. Open DevTools (F12) > Application > Local Storage")
        print("  3. Copy the 'token' value")
        print("\nThen set it:")
        print("  export QWEN_TOKEN='your_token_here'")
        return
    
    client = QwenClient(auth_token=token)
    
    print("=" * 60)
    print("  Qwen AI Chat Client")
    print("=" * 60)
    print()
    
    # Handle commands
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list-chats":
            print("Listing your chats...\n")
            try:
                chats = client.list_chats(page=1)
                if chats.get("success") and chats.get("data"):
                    for i, chat in enumerate(chats["data"], 1):
                        print(f"{i}. [{chat['id'][:16]}...] {chat.get('title', 'Untitled')}")
                        print(f"   Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(chat['created_at']))}")
                else:
                    print("No chats found")
            except Exception as e:
                print(f"Error: {e}")
        
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python qwen_client.py '<message>'        - Send a message")
            print("  python qwen_client.py --list-chats       - List your chats")
            print("  python qwen_client.py --help             - Show this help")
            print("\nExample:")
            print("  python qwen_client.py 'What is Python?'")
        
        else:
            # Send message
            message = " ".join(sys.argv[1:])
            print(f"You: {message}\n")
            print("AI: ", end="")
            try:
                response = client.chat(message)
                print()
            except Exception as e:
                print(f"\nError: {e}")
    else:
        print("Usage: python qwen_client.py '<your message>'")
        print("       python qwen_client.py --list-chats")
        print("       python qwen_client.py --help")
        print("\nExample:")
        print("  python qwen_client.py 'Hello, how are you?'")


if __name__ == "__main__":
    main()
