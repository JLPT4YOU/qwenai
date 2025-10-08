#!/usr/bin/env python3
"""Test advanced features: search, thinking, system prompt"""

import requests
import json

BASE_URL = "https://qwenai-two.vercel.app"

def test_advanced_chat():
    """Test chat with search, thinking, and system prompt"""
    print("=" * 70)
    print("🧪 Testing Advanced Features")
    print("=" * 70)
    
    # System prompt với icon và yêu cầu tóm tắt ngắn gọn
    system_prompt = """
Bạn là trợ lý AI thông minh. Khi trả lời:
- 📌 Tóm tắt ngắn gọn, súc tích
- 🔍 Sử dụng thông tin tìm kiếm nếu có
- 💡 Đưa ra câu trả lời chính xác
- ✨ Sử dụng icon để làm nổi bật thông tin
- 📊 Trình bày rõ ràng, dễ hiểu
"""
    
    # Câu hỏi thời sự
    message = "Tình hình kinh tế Việt Nam năm 2024 như thế nào? Tóm tắt ngắn gọn."
    
    payload = {
        "message": message,
        "model": "qwen-plus",  # Model hỗ trợ search
        "system_prompt": system_prompt,
        "thinking_enabled": True,
        "search_enabled": True,
        "stream": False
    }
    
    print(f"\n📝 Câu hỏi: {message}")
    print(f"🔧 Model: {payload['model']}")
    print(f"🧠 Thinking: {payload['thinking_enabled']}")
    print(f"🔍 Search: {payload['search_enabled']}")
    print(f"\n⏳ Đang gửi request...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/quick",
            json=payload,
            timeout=60  # Tăng timeout vì có search và thinking
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("\n" + "=" * 70)
                print("✅ KẾT QUẢ THÀNH CÔNG")
                print("=" * 70)
                
                response_data = data.get('data', {})
                
                # Hiển thị thinking process nếu có
                if 'thinking' in response_data and response_data['thinking']:
                    print("\n🧠 THINKING PROCESS:")
                    print("-" * 70)
                    print(response_data['thinking'])
                    print("-" * 70)
                
                # Hiển thị câu trả lời chính
                if 'content' in response_data:
                    print("\n💬 RESPONSE:")
                    print("-" * 70)
                    print(response_data['content'])
                    print("-" * 70)
                
                # Hiển thị chat_id
                if 'chat_id' in data:
                    print(f"\n🆔 Chat ID: {data['chat_id']}")
                
                print("\n✨ Test hoàn thành!")
                return True
            else:
                print(f"\n❌ Response không thành công: {data}")
                return False
        
        elif response.status_code == 403:
            print("\n⚠️  BỊ CHẶN BỞI SECURITY")
            print("-" * 70)
            error_data = response.json()
            print(f"Error: {error_data.get('error')}")
            print("\nℹ️  Lưu ý:")
            print("- API chỉ chấp nhận requests từ jlpt4you.com hoặc localhost")
            print("- Đảm bảo ENVIRONMENT=development trong Vercel")
            return False
        
        elif response.status_code == 401:
            print("\n⚠️  THIẾU TOKEN")
            print("-" * 70)
            print("Đảm bảo QWEN_TOKEN đã được set trong Vercel env vars")
            return False
        
        else:
            print(f"\n❌ LỖI: {response.status_code}")
            print("-" * 70)
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print("\n⏱️  TIMEOUT - Request quá lâu (>60s)")
        print("Có thể do search hoặc thinking mất nhiều thời gian")
        return False
    
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        return False

def test_simple_chat():
    """Test chat đơn giản không có search/thinking"""
    print("\n" + "=" * 70)
    print("🧪 Testing Simple Chat (no search/thinking)")
    print("=" * 70)
    
    payload = {
        "message": "Xin chào! Bạn là ai?",
        "model": "qwen-plus"
    }
    
    print(f"\n📝 Câu hỏi: {payload['message']}")
    print(f"⏳ Đang gửi request...\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/quick",
            json=payload,
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                content = data.get('data', {}).get('content', '')
                print(f"\n💬 Response: {content[:200]}...")
                return True
        
        print(f"\n❌ Failed: {response.text}")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("🚀 QWEN API - ADVANCED FEATURES TEST")
    print("=" * 70)
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 70)
    
    # Test 1: Simple chat
    result1 = test_simple_chat()
    
    # Test 2: Advanced features
    result2 = test_advanced_chat()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Simple Chat: {'✅ PASSED' if result1 else '❌ FAILED'}")
    print(f"Advanced Chat (Search + Thinking): {'✅ PASSED' if result2 else '❌ FAILED'}")
    print("=" * 70)

if __name__ == "__main__":
    main()
