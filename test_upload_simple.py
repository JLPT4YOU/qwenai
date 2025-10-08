"""
Simple Upload Test - Requires valid token
"""

import os
import sys

print("=" * 80)
print("🧪 FILE UPLOAD TEST")
print("=" * 80)

# Check token
token = os.getenv("QWEN_TOKEN")
if not token:
    print("\n❌ QWEN_TOKEN not set")
    print("\n📝 To get your token:")
    print("   1. Visit https://chat.qwen.ai")
    print("   2. Login to your account")
    print("   3. Open DevTools (F12)")
    print("   4. Go to Application → Local Storage")
    print("   5. Copy the 'token' value")
    print("\n💡 Then run:")
    print("   export QWEN_TOKEN='your_token_here'")
    print("   python test_upload_simple.py")
    sys.exit(1)

print(f"\n✓ Token found (length: {len(token)})")
print(f"  Preview: {token[:20]}...{token[-10:]}")

# Check files
image_path = "71xUvQRYnvL._SY466_.webp"
pdf_path = "Đề N3 7-2015-13-15.pdf"

if not os.path.exists(image_path):
    print(f"\n❌ Image not found: {image_path}")
    sys.exit(1)

if not os.path.exists(pdf_path):
    print(f"\n❌ PDF not found: {pdf_path}")
    sys.exit(1)

print(f"\n✓ Files found:")
print(f"  Image: {image_path} ({os.path.getsize(image_path):,} bytes)")
print(f"  PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")

# Import client
from qwen_client import QwenClient

print("\n" + "=" * 80)
print("TEST 1: Get STS Token")
print("=" * 80)

try:
    client = QwenClient(auth_token=token)
    print("\n📤 Requesting STS token for image...")
    
    sts_data = client.get_sts_token(
        filename=image_path,
        filesize=os.path.getsize(image_path),
        filetype="image"
    )
    
    print("\n✅ STS Token Response:")
    import json
    print(json.dumps(sts_data, indent=2))
    
    if sts_data.get('success') == False:
        print("\n❌ Failed to get STS token")
        print(f"   Error: {sts_data.get('data', {}).get('code')}")
        print(f"   Details: {sts_data.get('data', {}).get('details')}")
        print("\n💡 Your token may have expired. Please get a new token:")
        print("   1. Visit https://chat.qwen.ai")
        print("   2. Login again")
        print("   3. Get new token from DevTools")
        sys.exit(1)
    
    print("\n✓ STS token obtained successfully!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("TEST 2: Upload Image")
print("=" * 80)

try:
    print("\n📤 Uploading image...")
    file_metadata = client.upload_file(image_path, filetype="image")
    
    print("\n✅ Upload successful!")
    print(f"   File ID: {file_metadata['id']}")
    print(f"   File URL: {file_metadata['url'][:80]}...")
    print(f"   File Type: {file_metadata['file_type']}")
    print(f"   File Class: {file_metadata['file_class']}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("TEST 3: Chat with Image")
print("=" * 80)

try:
    print("\n💬 Sending message with image...")
    print("   Question: 'Mô tả chi tiết tấm ảnh này'")
    
    response = client.chat_with_files(
        message="Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
        files=[image_path],
        model="qwen3-max",
        stream=False
    )
    
    print("\n✅ Response received!")
    print("\n" + "-" * 80)
    print("🤖 AI Response:")
    print("-" * 80)
    print(response.get('content', 'No content'))
    print("-" * 80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("TEST 4: Upload PDF")
print("=" * 80)

try:
    print("\n📤 Uploading PDF...")
    file_metadata = client.upload_file(pdf_path, filetype="file")
    
    print("\n✅ Upload successful!")
    print(f"   File ID: {file_metadata['id']}")
    print(f"   File URL: {file_metadata['url'][:80]}...")
    print(f"   File Type: {file_metadata['file_type']}")
    print(f"   File Class: {file_metadata['file_class']}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("TEST 5: Chat with PDF")
print("=" * 80)

try:
    print("\n💬 Sending message with PDF...")
    print("   Question: 'Đây là đề thi gì? Tóm tắt nội dung'")
    
    response = client.chat_with_files(
        message="Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
        files=[pdf_path],
        model="qwen3-max",
        stream=False
    )
    
    print("\n✅ Response received!")
    print("\n" + "-" * 80)
    print("🤖 AI Response:")
    print("-" * 80)
    print(response.get('content', 'No content'))
    print("-" * 80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETED!")
print("=" * 80)
