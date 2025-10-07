"""
CORS Proxy Server for Qwen API
Allows browser to call Qwen API through this proxy
"""

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

QWEN_BASE_URL = "https://chat.qwen.ai/api"

@app.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS'])
def proxy(path):
    """Proxy all requests to Qwen API"""
    
    # Get authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No authorization header"}), 401
    
    # Build headers
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    
    # Add additional headers if present
    if request.headers.get('Accept'):
        headers['Accept'] = request.headers.get('Accept')
    if request.headers.get('source'):
        headers['source'] = request.headers.get('source')
    if request.headers.get('x-accel-buffering'):
        headers['x-accel-buffering'] = request.headers.get('x-accel-buffering')
    
    # Build URL
    url = f"{QWEN_BASE_URL}/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode()}"
    
    print(f"[PROXY] {request.method} {url}")
    
    try:
        # Handle OPTIONS preflight
        if request.method == 'OPTIONS':
            response = Response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, Accept, source, x-accel-buffering'
            return response
        
        # Make request to Qwen API
        if request.method == 'GET':
            resp = requests.get(url, headers=headers, stream=True)
        elif request.method == 'POST':
            data = request.get_json() if request.is_json else None
            resp = requests.post(url, headers=headers, json=data, stream=True)
        elif request.method == 'DELETE':
            resp = requests.delete(url, headers=headers)
        elif request.method == 'PUT':
            data = request.get_json() if request.is_json else None
            resp = requests.put(url, headers=headers, json=data)
        else:
            return jsonify({"error": "Method not allowed"}), 405
        
        # Handle streaming response
        if 'text/event-stream' in resp.headers.get('Content-Type', ''):
            def generate():
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk
            
            return Response(
                generate(),
                status=resp.status_code,
                headers={
                    'Content-Type': 'text/event-stream',
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': 'no-cache',
                    'X-Accel-Buffering': 'no'
                }
            )
        
        # Handle normal response
        return Response(
            resp.content,
            status=resp.status_code,
            headers={
                'Content-Type': resp.headers.get('Content-Type', 'application/json'),
                'Access-Control-Allow-Origin': '*'
            }
        )
        
    except requests.RequestException as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "proxy": "qwen-api"})

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    
    print("=" * 60)
    print("  Qwen API CORS Proxy Server")
    print("=" * 60)
    print(f"\n✓ Starting proxy server...")
    print(f"✓ Listening on: http://localhost:{port}")
    print("✓ Proxying to: https://chat.qwen.ai/api")
    print("\nUpdate index.html:")
    print(f"  const API_BASE = 'http://localhost:{port}/api';")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
