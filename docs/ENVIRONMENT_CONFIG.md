# 🔧 Environment Configuration Guide

## 📋 Overview

Dự án sử dụng environment variables để quản lý cấu hình, giúp:
- ✅ Bảo mật thông tin nhạy cảm (tokens, API keys)
- ✅ Dễ dàng chuyển đổi giữa môi trường (dev/prod)
- ✅ Tùy chỉnh URLs và endpoints
- ✅ Không hardcode values trong code

---

## 🚀 Quick Start

### 1. Copy file mẫu

```bash
cp .env.example .env
```

### 2. Cấu hình token

```bash
# Edit .env file
nano .env

# Thêm token của bạn
QWEN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Load environment variables

```bash
# Option 1: Export manually
export QWEN_TOKEN="your_token_here"

# Option 2: Use dotenv (recommended)
pip install python-dotenv
```

```python
# In your code
from dotenv import load_dotenv
load_dotenv()

import os
token = os.getenv("QWEN_TOKEN")
```

---

## 📝 Available Variables

### 🔑 Authentication

#### `QWEN_TOKEN` (Required)
- **Description**: JWT authentication token từ Qwen
- **Format**: String (JWT token)
- **Example**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **How to get**:
  1. Visit https://chat.qwen.ai
  2. Login to your account
  3. Open DevTools (F12)
  4. Go to Application → Local Storage
  5. Copy value of `token` key

**Usage:**
```python
from qwen_client import QwenClient

token = os.getenv("QWEN_TOKEN")
client = QwenClient(auth_token=token)
```

---

### 🌐 API Configuration

#### `QWEN_API_URL` (Optional)
- **Description**: Base URL cho Qwen API
- **Default**: `https://chat.qwen.ai/api`
- **Format**: URL string
- **Example**: `https://chat.qwen.ai/api`

**Use cases:**
- Custom proxy server
- Local development server
- Alternative endpoints

**Usage:**
```python
# Automatically loaded from environment
client = QwenClient(auth_token=token)
# Uses QWEN_API_URL if set, otherwise default

# Or override manually
client = QwenClient(
    auth_token=token,
    base_url="https://custom-proxy.com/api"
)
```

**Example with proxy:**
```bash
# .env
QWEN_API_URL=https://my-proxy.com/qwen-api
```

---

### 🔐 Security

#### `ADMIN_KEY` (Required for production)
- **Description**: Secret key để update token qua API
- **Default**: `change-me-in-production`
- **Format**: Random string
- **Example**: `sk_live_a1b2c3d4e5f6g7h8i9j0`

**Generate secure key:**
```bash
# Option 1: OpenSSL
openssl rand -hex 32

# Option 2: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: UUID
python -c "import uuid; print(str(uuid.uuid4()))"
```

**Usage:**
```bash
# Update token via API
curl -X POST http://localhost:5001/api/admin/token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "new_token_here",
    "admin_key": "your_admin_key"
  }'
```

---

### 🏗️ Server Configuration

#### `ENVIRONMENT` (Optional)
- **Description**: Môi trường chạy server
- **Default**: `development`
- **Options**: `development`, `production`
- **Example**: `production`

**Behavior:**
- `development`: API endpoints accessible, CORS relaxed
- `production`: API restricted, CORS strict

**Usage:**
```bash
# Development
ENVIRONMENT=development python api_server.py

# Production
ENVIRONMENT=production python api_server.py
```

---

## 📁 File Structure

```
.env.example          # Template file (commit to git)
.env                  # Your actual config (DO NOT commit)
.gitignore           # Should include .env
```

**`.gitignore` should contain:**
```
.env
.token_storage.json
*.pyc
__pycache__/
```

---

## 🔒 Security Best Practices

### 1. Never commit `.env` file

```bash
# Check if .env is ignored
git status

# If not, add to .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

### 2. Use different tokens for dev/prod

```bash
# Development
QWEN_TOKEN=dev_token_here

# Production
QWEN_TOKEN=prod_token_here
```

### 3. Rotate tokens regularly

```bash
# Get new token from Qwen
# Update .env
# Restart server
```

### 4. Use strong admin keys

```bash
# Bad
ADMIN_KEY=admin123

# Good - Use a long random string
ADMIN_KEY=your_secure_random_string_here_min_32_chars
```

### 5. Restrict file permissions

```bash
# Only owner can read/write
chmod 600 .env
```

---

## 🎯 Usage Examples

### Example 1: Basic Setup

```bash
# .env
QWEN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

```python
# app.py
import os
from qwen_client import QwenClient

token = os.getenv("QWEN_TOKEN")
client = QwenClient(auth_token=token)

response = client.chat("Hello!")
print(response)
```

### Example 2: Custom API URL

```bash
# .env
QWEN_TOKEN=your_token
QWEN_API_URL=https://my-proxy.com/api
```

```python
# Client automatically uses QWEN_API_URL
client = QwenClient(auth_token=os.getenv("QWEN_TOKEN"))
```

### Example 3: Production Setup

```bash
# .env.production
QWEN_TOKEN=prod_token_here
QWEN_API_URL=https://chat.qwen.ai/api
ADMIN_KEY=sk_live_secure_random_key_here
ENVIRONMENT=production
```

```bash
# Load production config
export $(cat .env.production | xargs)
python api_server.py 5001
```

### Example 4: Multiple Environments

```bash
# .env.development
QWEN_TOKEN=dev_token
ENVIRONMENT=development

# .env.staging
QWEN_TOKEN=staging_token
ENVIRONMENT=production

# .env.production
QWEN_TOKEN=prod_token
ENVIRONMENT=production
```

```bash
# Load specific environment
export $(cat .env.development | xargs)
python api_server.py
```

---

## 🐳 Docker Support

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Environment variables will be passed at runtime
CMD ["python", "api_server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  qwen-api:
    build: .
    ports:
      - "5001:5001"
    environment:
      - QWEN_TOKEN=${QWEN_TOKEN}
      - QWEN_API_URL=${QWEN_API_URL:-https://chat.qwen.ai/api}
      - ADMIN_KEY=${ADMIN_KEY}
      - ENVIRONMENT=${ENVIRONMENT:-development}
    env_file:
      - .env
```

### Run with Docker

```bash
# Build
docker-compose build

# Run with .env file
docker-compose up

# Or pass env vars directly
docker run -e QWEN_TOKEN=your_token qwen-api
```

---

## 🔧 Troubleshooting

### Issue 1: Token not found

**Error:**
```
ValueError: No token available
```

**Solution:**
```bash
# Check if QWEN_TOKEN is set
echo $QWEN_TOKEN

# If empty, set it
export QWEN_TOKEN="your_token"

# Or add to .env
echo "QWEN_TOKEN=your_token" >> .env
```

### Issue 2: Wrong API URL

**Error:**
```
requests.exceptions.ConnectionError: Failed to connect
```

**Solution:**
```bash
# Check current URL
echo $QWEN_API_URL

# Reset to default
unset QWEN_API_URL

# Or set correct URL
export QWEN_API_URL="https://chat.qwen.ai/api"
```

### Issue 3: Permission denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: '.env'
```

**Solution:**
```bash
# Fix permissions
chmod 600 .env

# Check owner
ls -la .env
```

### Issue 4: Environment not loading

**Solution:**
```python
# Install python-dotenv
pip install python-dotenv

# Load in code
from dotenv import load_dotenv
load_dotenv()

# Verify
import os
print(os.getenv("QWEN_TOKEN"))
```

---

## 📚 Advanced Configuration

### Load from custom file

```python
from dotenv import load_dotenv

# Load from custom file
load_dotenv('.env.production')

# Or specify path
load_dotenv('/path/to/.env')
```

### Override existing variables

```python
# Don't override existing env vars
load_dotenv(override=False)

# Override existing env vars
load_dotenv(override=True)
```

### Validate configuration

```python
import os

def validate_config():
    """Validate required environment variables"""
    required = ['QWEN_TOKEN']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing required env vars: {missing}")
    
    # Validate token format
    token = os.getenv('QWEN_TOKEN')
    if not token.startswith('eyJ'):
        raise ValueError("Invalid token format")
    
    print("✓ Configuration valid")

validate_config()
```

### Dynamic configuration

```python
class Config:
    """Configuration manager"""
    
    def __init__(self):
        self.token = os.getenv('QWEN_TOKEN')
        self.api_url = os.getenv('QWEN_API_URL', 'https://chat.qwen.ai/api')
        self.admin_key = os.getenv('ADMIN_KEY', 'change-me')
        self.environment = os.getenv('ENVIRONMENT', 'development')
    
    @property
    def is_production(self):
        return self.environment == 'production'
    
    def validate(self):
        if not self.token:
            raise ValueError("QWEN_TOKEN not set")
        
        if self.is_production and self.admin_key == 'change-me':
            raise ValueError("Change ADMIN_KEY in production")

# Usage
config = Config()
config.validate()

client = QwenClient(
    auth_token=config.token,
    base_url=config.api_url
)
```

---

## 📖 Summary

### Required Variables
- ✅ `QWEN_TOKEN` - Your authentication token

### Optional Variables
- ⚙️ `QWEN_API_URL` - Custom API endpoint
- 🔐 `ADMIN_KEY` - Admin authentication
- 🏗️ `ENVIRONMENT` - dev/prod mode

### Best Practices
- 🔒 Never commit `.env` to git
- 🔑 Use strong admin keys
- 🔄 Rotate tokens regularly
- 📝 Document all variables
- ✅ Validate configuration on startup

---

## 🔗 Related Documentation

- **Quick Start**: `/QUICKSTART.md`
- **Security Config**: `/SECURITY_CONFIG.md`
- **API Guide**: `/docs/FILE_UPLOAD_API.md`
