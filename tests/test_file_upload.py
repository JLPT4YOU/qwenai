"""
Test file upload functionality
"""

import os
import sys
import requests
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qwen_client import QwenClient

def test_upload_image():
    """Test uploading an image file"""
    token = os.getenv("QWEN_TOKEN")
    if not token:
        print("❌ QWEN_TOKEN not set")
        return False
    
    print("=" * 60)
    print("Test 1: Upload Image File")
    print("=" * 60)
    
    try:
        client = QwenClient(auth_token=token)
        
        # Create a test image file
        test_image_path = "/tmp/test_image.png"
        
        # Create a simple 1x1 PNG image
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        with open(test_image_path, 'wb') as f:
            f.write(png_data)
        
        print(f"\n1. Created test image: {test_image_path}")
        print(f"   Size: {len(png_data)} bytes")
        
        # Upload the file
        print("\n2. Uploading file...")
        file_metadata = client.upload_file(test_image_path, filetype="image")
        
        print("\n✓ Upload successful!")
        print(f"   File ID: {file_metadata['id']}")
        print(f"   File URL: {file_metadata['url'][:80]}...")
        print(f"   File Type: {file_metadata['file_type']}")
        print(f"   File Class: {file_metadata['file_class']}")
        print(f"   Status: {file_metadata['status']}")
        
        # Clean up
        os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_with_image():
    """Test sending a chat message with an image"""
    token = os.getenv("QWEN_TOKEN")
    if not token:
        print("❌ QWEN_TOKEN not set")
        return False
    
    print("\n" + "=" * 60)
    print("Test 2: Chat with Image")
    print("=" * 60)
    
    try:
        client = QwenClient(auth_token=token)
        
        # Create a test image
        test_image_path = "/tmp/test_chat_image.png"
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        with open(test_image_path, 'wb') as f:
            f.write(png_data)
        
        print(f"\n1. Created test image: {test_image_path}")
        
        # Send message with image
        print("\n2. Sending message with image...")
        print("   Message: 'What do you see in this image?'")
        
        response = client.chat_with_files(
            message="What do you see in this image?",
            files=[test_image_path],
            model="qwen3-max",
            stream=False
        )
        
        print("\n✓ Response received!")
        print(f"\nAI Response:\n{response.get('content', 'No content')[:200]}...")
        
        # Clean up
        os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_upload():
    """Test file upload via API endpoint"""
    token = os.getenv("QWEN_TOKEN")
    if not token:
        print("❌ QWEN_TOKEN not set")
        return False
    
    print("\n" + "=" * 60)
    print("Test 3: API File Upload")
    print("=" * 60)
    
    try:
        # Create a test file
        test_file_path = "/tmp/test_api_upload.txt"
        with open(test_file_path, 'w') as f:
            f.write("This is a test file for API upload.")
        
        print(f"\n1. Created test file: {test_file_path}")
        
        # Upload via API
        print("\n2. Uploading via API endpoint...")
        
        with open(test_file_path, 'rb') as f:
            response = requests.post(
                "http://localhost:5001/api/files/upload",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                files={
                    "file": ("test.txt", f, "text/plain")
                },
                data={
                    "filetype": "file"
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Upload successful!")
            print(f"   File ID: {data['data']['id']}")
            print(f"   File URL: {data['data']['url'][:80]}...")
            print(f"   Status: {data['data']['status']}")
        else:
            print(f"\n❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Clean up
        os.remove(test_file_path)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_get_sts_token():
    """Test getting STS token"""
    token = os.getenv("QWEN_TOKEN")
    if not token:
        print("❌ QWEN_TOKEN not set")
        return False
    
    print("\n" + "=" * 60)
    print("Test 4: Get STS Token")
    print("=" * 60)
    
    try:
        client = QwenClient(auth_token=token)
        
        print("\n1. Requesting STS token...")
        sts_data = client.get_sts_token(
            filename="test.png",
            filesize=1024,
            filetype="image"
        )
        
        print("\n✓ STS token received!")
        print(f"   File ID: {sts_data.get('file_id')}")
        print(f"   Bucket: {sts_data.get('bucket')}")
        print(f"   Region: {sts_data.get('region')}")
        print(f"   Endpoint: {sts_data.get('endpoint')}")
        print(f"   Expiration: {sts_data.get('expiration')}")
        print(f"   Access Key ID: {sts_data.get('access_key_id', '')[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  Qwen File Upload Tests")
    print("=" * 60)
    
    # Check if oss2 is installed
    try:
        import oss2
        print("\n✓ oss2 package is installed")
    except ImportError:
        print("\n⚠️  Warning: oss2 package not installed")
        print("   Install with: pip install oss2")
        print("   Some tests will fail without this package\n")
    
    results = []
    
    # Run tests
    results.append(("Get STS Token", test_get_sts_token()))
    
    # Only run upload tests if oss2 is available
    try:
        import oss2
        results.append(("Upload Image", test_upload_image()))
        results.append(("Chat with Image", test_chat_with_image()))
        results.append(("API Upload", test_api_upload()))
    except ImportError:
        print("\n⚠️  Skipping upload tests (oss2 not installed)")
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}  {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
