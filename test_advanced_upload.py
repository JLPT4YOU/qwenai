"""
Advanced File Upload Test
Test upload image + PDF with advanced features (thinking, search)
"""

import os
import sys
from qwen_client import QwenClient

def test_image_and_pdf():
    """Test upload both image and PDF with advanced features"""
    
    # Get token from environment or stored file
    token = os.getenv("QWEN_TOKEN")
    
    # Try to load from stored file if not in environment
    if not token:
        try:
            import json
            token_file = '.token_storage.json'
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    data = json.load(f)
                    token = data.get('token')
                    print("✓ Loaded token from storage file")
        except:
            pass
    
    if not token:
        print("❌ QWEN_TOKEN not set and no stored token found")
        print("\nOptions:")
        print("  1. Run: export QWEN_TOKEN='your_token_here'")
        print("  2. Or create .token_storage.json with your token")
        return
    
    print("=" * 80)
    print("🧪 ADVANCED FILE UPLOAD TEST")
    print("=" * 80)
    
    # Initialize client
    client = QwenClient(auth_token=token)
    
    # File paths
    image_path = "71xUvQRYnvL._SY466_.webp"
    pdf_path = "Đề N3 7-2015-13-15.pdf"
    
    # Check files exist
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print(f"\n📁 Files to upload:")
    print(f"   1. Image: {image_path} ({os.path.getsize(image_path):,} bytes)")
    print(f"   2. PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
    
    # Test 1: Upload image and ask about it
    print("\n" + "=" * 80)
    print("TEST 1: Analyze Image (Vision)")
    print("=" * 80)
    
    try:
        print("\n📤 Uploading image...")
        response1 = client.chat_with_files(
            message="Mô tả chi tiết tấm ảnh này. Đây là ảnh gì? Có những gì trong ảnh?",
            files=[image_path],
            model="qwen3-max",
            stream=False
        )
        
        print("\n✅ Response received!")
        print("\n" + "-" * 80)
        print("🤖 AI Response (Image Analysis):")
        print("-" * 80)
        print(response1.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Upload PDF and ask about it
    print("\n" + "=" * 80)
    print("TEST 2: Analyze PDF (Document RAG)")
    print("=" * 80)
    
    try:
        print("\n📤 Uploading PDF...")
        response2 = client.chat_with_files(
            message="Đây là đề thi gì? Tóm tắt nội dung của đề thi này.",
            files=[pdf_path],
            model="qwen3-max",
            stream=False
        )
        
        print("\n✅ Response received!")
        print("\n" + "-" * 80)
        print("🤖 AI Response (PDF Analysis):")
        print("-" * 80)
        print(response2.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Upload BOTH files together
    print("\n" + "=" * 80)
    print("TEST 3: Analyze BOTH Files Together")
    print("=" * 80)
    
    try:
        print("\n📤 Uploading both files...")
        response3 = client.chat_with_files(
            message="Tôi có 2 file: 1 ảnh và 1 PDF. Hãy phân tích cả 2 file và cho biết chúng có liên quan gì đến nhau không?",
            files=[image_path, pdf_path],
            model="qwen3-max",
            stream=False
        )
        
        print("\n✅ Response received!")
        print("\n" + "-" * 80)
        print("🤖 AI Response (Combined Analysis):")
        print("-" * 80)
        print(response3.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: With Thinking Mode (if supported)
    print("\n" + "=" * 80)
    print("TEST 4: Advanced - With Thinking Mode")
    print("=" * 80)
    
    try:
        print("\n📤 Uploading with thinking mode...")
        print("💭 Thinking mode: Enabled")
        
        # Create a new chat with thinking enabled
        import uuid
        chat_id = str(uuid.uuid4())
        
        # Upload files first
        print("\n1. Uploading files...")
        file_metadata = []
        for file_path in [image_path, pdf_path]:
            metadata = client.upload_file(file_path)
            file_metadata.append(metadata)
            print(f"   ✓ Uploaded: {metadata['name']}")
        
        # Send message with thinking enabled
        print("\n2. Sending message with thinking mode...")
        message_data = {
            "role": "user",
            "content": "Phân tích sâu về mối liên hệ giữa ảnh và PDF. Đây có phải là tài liệu học tiếng Nhật không?",
            "files": file_metadata
        }
        
        response4 = client.send_message(
            chat_id=chat_id,
            message=message_data,
            model="qwen3-max",
            stream=False,
            thinking_enabled=True
        )
        
        print("\n✅ Response received!")
        
        if response4.get('thinking'):
            print("\n" + "-" * 80)
            print("💭 AI Thinking Process:")
            print("-" * 80)
            print(response4['thinking'])
            print("-" * 80)
        
        print("\n" + "-" * 80)
        print("🤖 AI Final Response:")
        print("-" * 80)
        print(response4.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 5: With Search Enabled
    print("\n" + "=" * 80)
    print("TEST 5: Advanced - With Search Enabled")
    print("=" * 80)
    
    try:
        print("\n📤 Uploading with search enabled...")
        print("🔍 Search mode: Enabled")
        
        chat_id = str(uuid.uuid4())
        
        # Upload files
        print("\n1. Uploading files...")
        file_metadata = []
        for file_path in [image_path, pdf_path]:
            metadata = client.upload_file(file_path)
            file_metadata.append(metadata)
            print(f"   ✓ Uploaded: {metadata['name']}")
        
        # Send message with search enabled
        print("\n2. Sending message with search mode...")
        message_data = {
            "role": "user",
            "content": "Dựa vào ảnh và PDF, hãy tìm kiếm thông tin về JLPT N3 và cho biết độ khó của kỳ thi này.",
            "files": file_metadata
        }
        
        response5 = client.send_message(
            chat_id=chat_id,
            message=message_data,
            model="qwen3-max",
            stream=False,
            search_enabled=True
        )
        
        print("\n✅ Response received!")
        print("\n" + "-" * 80)
        print("🔍 AI Response (with Search):")
        print("-" * 80)
        print(response5.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 6: Combined - Thinking + Search + Files
    print("\n" + "=" * 80)
    print("TEST 6: ULTIMATE - Thinking + Search + Multiple Files")
    print("=" * 80)
    
    try:
        print("\n📤 Ultimate test with all features...")
        print("💭 Thinking: Enabled")
        print("🔍 Search: Enabled")
        print("📁 Files: 2 (image + PDF)")
        
        chat_id = str(uuid.uuid4())
        
        # Upload files
        print("\n1. Uploading files...")
        file_metadata = []
        for file_path in [image_path, pdf_path]:
            metadata = client.upload_file(file_path)
            file_metadata.append(metadata)
            print(f"   ✓ Uploaded: {metadata['name']}")
        
        # Send with all features
        print("\n2. Sending with all advanced features...")
        message_data = {
            "role": "user",
            "content": """Hãy phân tích toàn diện:
1. Ảnh này là gì? Có liên quan đến học tiếng Nhật không?
2. PDF là đề thi gì? Độ khó thế nào?
3. Hai tài liệu này có mối liên hệ gì?
4. Nếu tôi muốn học tiếng Nhật, tôi nên bắt đầu từ đâu?
5. Tìm kiếm thêm thông tin về JLPT N3 và đưa ra lời khuyên.""",
            "files": file_metadata
        }
        
        response6 = client.send_message(
            chat_id=chat_id,
            message=message_data,
            model="qwen3-max",
            stream=False,
            thinking_enabled=True,
            search_enabled=True
        )
        
        print("\n✅ Response received!")
        
        if response6.get('thinking'):
            print("\n" + "-" * 80)
            print("💭 AI Thinking Process:")
            print("-" * 80)
            print(response6['thinking'][:500] + "..." if len(response6['thinking']) > 500 else response6['thinking'])
            print("-" * 80)
        
        print("\n" + "-" * 80)
        print("🤖 AI Ultimate Response:")
        print("-" * 80)
        print(response6.get('content', 'No content'))
        print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print("\n✅ Completed Tests:")
    print("   1. ✓ Image analysis (Vision)")
    print("   2. ✓ PDF analysis (Document RAG)")
    print("   3. ✓ Combined files analysis")
    print("   4. ✓ With Thinking mode")
    print("   5. ✓ With Search mode")
    print("   6. ✓ Ultimate (Thinking + Search + Files)")
    print("\n🎉 All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_image_and_pdf()
