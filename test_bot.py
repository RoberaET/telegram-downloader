#!/usr/bin/env python3
"""
Test script for TikTok Downloader functionality
This script tests the core downloading functionality without running the Telegram bot
"""

import os
import sys
import config
from bot import TikTokDownloader

def test_tiktok_downloader():
    """Test the TikTok downloader functionality"""
    print("🧪 Testing TikTok Downloader...")
    
    # Initialize downloader
    downloader = TikTokDownloader()
    
    # Test URL validation
    print("\n1. Testing URL validation...")
    test_urls = [
        "https://www.tiktok.com/@username/video/1234567890",
        "https://vm.tiktok.com/xxxxx/",
        "https://vt.tiktok.com/xxxxx/",
        "https://youtube.com/watch?v=123",
        "https://example.com",
        "not a url"
    ]
    
    for url in test_urls:
        is_valid = downloader.is_tiktok_url(url)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {url}")
    
    # Test video info extraction (with a sample URL)
    print("\n2. Testing video info extraction...")
    sample_url = "https://www.tiktok.com/@tiktok/video/1234567890"
    
    try:
        info = downloader.get_video_info(sample_url)
        if info:
            print("   ✅ Video info extraction works")
            print(f"   📊 Video ID: {info.get('id', 'N/A')}")
            print(f"   📝 Title: {info.get('title', 'N/A')[:50]}...")
        else:
            print("   ❌ Could not extract video info")
    except Exception as e:
        print(f"   ❌ Error during video info extraction: {e}")
    
    print("\n3. Testing configuration...")
    print(f"   📏 Max file size: {downloader.max_file_size} bytes ({downloader.max_file_size / 1024 / 1024:.1f} MB)")
    print(f"   ⏱️  Download timeout: {downloader.download_timeout} seconds")
    
    print("\n✅ TikTok Downloader test completed!")
    print("\n📝 Note: This test doesn't actually download videos.")
    print("   To test full functionality, run the bot with a real TikTok URL.")

def test_environment():
    """Test if all required dependencies are available"""
    print("🔍 Testing environment...")
    
    required_modules = [
        'telegram',
        'yt_dlp',
        'requests',
        'dotenv',
        'aiohttp',
        'asyncio'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - NOT FOUND")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("   Please install missing dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required modules are available!")
        return True

def main():
    """Main test function"""
    print("🚀 TikTok Downloader Bot - Test Suite")
    print("=" * 50)
    
    # Test environment first
    if not test_environment():
        sys.exit(1)
    
    # Test downloader functionality
    test_tiktok_downloader()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📋 Next steps:")
    print("1. Your bot token is already configured in config.py")
    print("2. Run: python bot.py")
    print("3. Test with a real TikTok URL in Telegram")

if __name__ == "__main__":
    main() 