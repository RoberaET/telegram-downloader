#!/usr/bin/env python3
"""
Quick test to verify bot configuration and connectivity
"""

import config
import requests
import json

def test_bot_connection():
    """Test if the bot token is valid and bot is accessible"""
    print("🔍 Testing bot connection...")
    
    token = config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Bot connection successful!")
                print(f"   🤖 Bot Name: {bot_info.get('first_name', 'N/A')}")
                print(f"   📝 Username: @{bot_info.get('username', 'N/A')}")
                print(f"   🆔 Bot ID: {bot_info.get('id', 'N/A')}")
                print(f"   🔗 Bot Link: https://t.me/{bot_info.get('username', 'N/A')}")
                return True
            else:
                print(f"❌ Bot API error: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_config():
    """Test configuration values"""
    print("\n⚙️ Testing configuration...")
    print(f"   🔑 Token: {config.TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"   📏 Max file size: {config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB")
    print(f"   ⏱️  Timeout: {config.DOWNLOAD_TIMEOUT} seconds")
    print("✅ Configuration loaded successfully!")

def main():
    print("🚀 Quick Bot Test")
    print("=" * 40)
    
    test_config()
    
    if test_bot_connection():
        print("\n🎉 Bot is ready to use!")
        print("\n📱 To test the bot:")
        print("1. Open Telegram")
        print("2. Search for your bot username")
        print("3. Send /start to begin")
        print("4. Send a TikTok URL to test downloading")
    else:
        print("\n❌ Bot connection failed!")
        print("Please check your bot token in config.py")

if __name__ == "__main__":
    main() 