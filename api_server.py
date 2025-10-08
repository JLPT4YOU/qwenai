"""
Qwen API Backend Server
Full REST API wrapper around qwen_client.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from qwen_client import QwenClient
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Cache for clients
_client_cache = {}

# Token storage file (for persistence)
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '.token_storage.json')

def load_stored_token():
    """Load token from file"""
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'r') as f:
                data = json.load(f)
                return data.get('token')
        except:
            pass
    return None

def save_token(token):
    """Save token to file"""
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'token': token, 'updated_at': int(time.time())}, f)

# Global client instance (will be initialized per request with token)
def get_token_from_request():
    """
    Get token from request or environment variable
    Priority: 
    1. Authorization header from user
    2. QWEN_TOKEN from environment variable
    3. Stored token from file
    """
    # Try to get from Authorization header
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token:
        return token
    
    # Try to get from environment variable
    env_token = os.getenv('QWEN_TOKEN')
    if env_token:
        return env_token
    
    # Try to get from stored file
    stored_token = load_stored_token()
    if stored_token:
        return stored_token
    
    return None

def get_client(token=None):
    """Get QwenClient instance with token"""
    if not token:
        token = get_token_from_request()
    
    if not token:
        raise ValueError("No token available")
    
    if token in _client_cache:
        return _client_cache[token]
    client = QwenClient(auth_token=token)
    _client_cache[token] = client
    return client

# Health & Status Endpoints
# ============================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "qwen-api-server",
        "timestamp": int(time.time())
    })

@app.route('/api/models', methods=['GET'])
def list_models():
    """List available Qwen models"""
    try:
        client = get_client()
        models = client.list_models()
        return jsonify(models)
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/token', methods=['POST'])
def update_token():
    """
    Update server token (for admin use)
    Requires admin_key for security
    
    POST /api/admin/token
    {
        "token": "new-token",
        "admin_key": "your-secret-key"
    }
    """
    data = request.get_json()
    admin_key = data.get('admin_key')
    new_token = data.get('token')
    
    # Check admin key (set via env var)
    expected_key = os.getenv('ADMIN_KEY', 'change-me-in-production')
    if admin_key != expected_key:
        return jsonify({"error": "Invalid admin key"}), 403
    
    if not new_token:
        return jsonify({"error": "Token required"}), 400
    
    # Save token
    save_token(new_token)
    
    # Clear cache so new token is used
    _client_cache.clear()
    
    return jsonify({
        "success": True,
        "message": "Token updated successfully",
        "timestamp": int(time.time())
    })

@app.route('/api/admin/token', methods=['GET'])
def get_token_info():
    """Get stored token info (masked for security)"""
    admin_key = request.args.get('admin_key')
    expected_key = os.getenv('ADMIN_KEY', 'change-me-in-production')
    
    if admin_key != expected_key:
        return jsonify({"error": "Invalid admin key"}), 403
    
    stored = load_stored_token()
    if stored:
        masked = stored[:20] + '...' + stored[-10:] if len(stored) > 30 else stored[:10] + '...'
        return jsonify({
            "has_token": True,
            "token_preview": masked
        })
    else:
        return jsonify({
            "has_token": False
        })

@app.route('/api/user/status', methods=['GET'])
def user_status():
    """Get user status"""
    try:
        client = get_client()
        status = client.get_user_status()
        return jsonify(status)
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# ============================================================

@app.route('/api/token/refresh', methods=['POST'])
def refresh_token():
    """Refresh authentication token"""
    try:
        client = get_client()
        new_token = client.refresh_token()
        
        # Save the new token
        save_token(new_token)
        
        return jsonify({
            "success": True,
            "token": new_token,
            "message": "Token refreshed successfully"
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/token/info', methods=['GET'])
def token_info():
    """Get token information"""
    try:
        token = get_token_from_request()
        if not token:
            return jsonify({"error": "No authorization token"}), 401
        
        return jsonify({
            "token_length": len(token),
            "token_preview": token[:10] + "..." + token[-10:] if len(token) > 20 else "***",
            "has_token": True,
            "source": "header" if request.headers.get('Authorization') else "environment"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Chat Management
# ============================================================

@app.route('/api/chats', methods=['GET'])
def list_chats():
    """List all chats"""
    page = request.args.get('page', 1, type=int)
    
    try:
        client = get_client()
        chats = client.list_chats(page=page)
        return jsonify({
            "success": True,
            "data": chats.get('data', []),
            "total": len(chats.get('data', []))
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Get chat history"""
    try:
        client = get_client()
        history = client.get_chat_history(chat_id)
        return jsonify({
            "success": True,
            "data": history
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """Delete a chat"""
    try:
        client = get_client()
        success = client.delete_chat(chat_id)
        return jsonify({
            "success": success,
            "message": "Chat deleted successfully" if success else "Failed to delete chat"
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Messaging
# ============================================================

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    """
    Send a message to chat
    
    Request body:
    {
        "chat_id": "chat-id",
        "message": "your message",
        "model": "qwen3-max",  // optional
        "stream": false  // always false for now
    }
    """
    data = request.get_json()
    chat_id = data.get('chat_id')
    message = data.get('message')
    model = data.get('model', 'qwen3-max')
    system_prompt = data.get('system_prompt')
    thinking_enabled = data.get('thinking_enabled', False)
    search_enabled = data.get('search_enabled', False)
    
    if not chat_id or not message:
        return jsonify({"error": "chat_id and message are required"}), 400
    
    try:
        client = get_client()
        
        # Capture stdout to get the streamed response
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Call with stream=True to get response content
            result = client.send_message(
                chat_id=chat_id,
                message=message,
                model=model,
                stream=True,
                system_prompt=system_prompt,
                thinking_enabled=thinking_enabled,
                search_enabled=search_enabled
            )
            
            # Get the captured output
            response_content = sys.stdout.getvalue()
            
        finally:
            sys.stdout = old_stdout
        
        # Return the response with thinking if available
        response_data = {
            "content": result.get("content", response_content.strip())
        }
        
        # Add thinking content if present
        if "thinking" in result and result["thinking"]:
            response_data["thinking"] = result["thinking"]
        
        return jsonify({
            "success": True,
            "data": response_data
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/quick', methods=['POST'])
def quick_chat():
    """
    Quick chat - sends message to most recent chat
    
    Request body:
    {
        "message": "your message",
        "model": "qwen3-max"  // optional
    }
    """
    data = request.get_json()
    message = data.get('message')
    model = data.get('model', 'qwen3-max')
    system_prompt = data.get('system_prompt')
    thinking_enabled = data.get('thinking_enabled', False)
    search_enabled = data.get('search_enabled', False)
    
    if not message:
        return jsonify({"error": "message is required"}), 400
    
    try:
        client = get_client()
        
        # Get most recent chat
        chats = client.list_chats(page=1)
        if not chats.get('data'):
            return jsonify({"error": "No chats found. Please create a chat first."}), 404
        
        chat_id = chats['data'][0]['id']
        
        # Capture stdout to get the streamed response
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Call with stream=True to get response content
            result = client.send_message(
                chat_id=chat_id,
                message=message,
                model=model,
                stream=True,
                system_prompt=system_prompt,
                thinking_enabled=thinking_enabled,
                search_enabled=search_enabled
            )
            
            # Get the captured output
            response_content = sys.stdout.getvalue()
            
        finally:
            sys.stdout = old_stdout
        
        # Return response with thinking if available
        response_data = {
            "content": result.get("content", response_content.strip())
        }
        
        if "thinking" in result and result["thinking"]:
            response_data["thinking"] = result["thinking"]
        
        return jsonify({
            "success": True,
            "chat_id": chat_id,
            "data": response_data
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ============================================================
# Statistics & Info
# ============================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get user statistics"""
    try:
        client = get_client()
        
        # Get chats
        chats = client.list_chats(page=1)
        chat_count = len(chats.get('data', []))
        
        # Get user info
        info = client.get_token_info()
        
        return jsonify({
            "success": True,
            "stats": {
                "total_chats": chat_count,
                "user": {
                    "name": info.get('name'),
                    "email": info.get('email')
                },
                "token_expires_at": info.get('expires_at')
            }
        })
    except ValueError as e:
        return jsonify({"error": "No authorization token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    
    print("=" * 60)
    print("  Qwen API Backend Server")
    print("=" * 60)
    print(f"\n✓ Starting API server...")
    print(f"✓ Listening on: http://localhost:{port}")
    print(f"✓ CORS enabled for all origins")
    print("\n📚 Available Endpoints:")
    print(f"  GET  /health                    - Health check")
    print(f"  GET  /api/user/status           - User status")
    print(f"  POST /api/token/refresh         - Refresh token")
    print(f"  GET  /api/token/info            - Token info")
    print(f"  GET  /api/chats                 - List chats")
    print(f"  GET  /api/chats/<id>            - Get chat history")
    print(f"  DELETE /api/chats/<id>          - Delete chat")
    print(f"  POST /api/chat/send             - Send message")
    print(f"  POST /api/chat/quick            - Quick chat")
    print(f"  GET  /api/stats                 - Get statistics")
    print("\n💡 Usage:")
    print(f"  curl -H 'Authorization: Bearer <token>' http://localhost:{port}/api/chats")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
