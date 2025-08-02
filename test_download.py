#!/usr/bin/env python3
"""
Test script to debug TikTok download issues
"""

import yt_dlp
import os
import sys

def test_tiktok_download(url):
    """Test downloading a TikTok video"""
    print(f"🧪 Testing download for: {url}")
    
    # Test video info extraction
    print("\n1. Testing video info extraction...")
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                print(f"✅ Video info extracted successfully!")
                print(f"   📝 Title: {info.get('title', 'N/A')}")
                print(f"   🆔 ID: {info.get('id', 'N/A')}")
                print(f"   👤 Uploader: {info.get('uploader', 'N/A')}")
                print(f"   📊 Duration: {info.get('duration', 'N/A')} seconds")
            else:
                print("❌ Could not extract video info")
                return False
    except Exception as e:
        print(f"❌ Error extracting video info: {e}")
        return False
    
    # Test actual download
    print("\n2. Testing video download...")
    output_path = "test_video.mp4"
    
    try:
        ydl_opts = {
            'format': 'best[filesize<50M]/best',
            'outtmpl': output_path,
            'quiet': False,  # Show progress
            'no_warnings': False,
            'extract_flat': False,
            'no_check_certificate': True,
            'ignoreerrors': False,
            'nocheckcertificate': True,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'geo_bypass_ip_block': '1.0.0.1',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Download successful!")
            print(f"   📁 File: {output_path}")
            print(f"   📏 Size: {file_size} bytes ({file_size / 1024 / 1024:.1f} MB)")
            
            # Clean up
            os.remove(output_path)
            print(f"   🧹 Cleaned up test file")
            return True
        else:
            print("❌ Download failed - file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error during download: {e}")
        return False

def main():
    """Main function"""
    print("🚀 TikTok Download Test")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter TikTok URL to test: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    success = test_tiktok_download(url)
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Your bot should work with this URL.")
    else:
        print("\n❌ Test failed!")
        print("This might be due to:")
        print("• Private video")
        print("• Region restrictions")
        print("• TikTok API changes")
        print("• Network issues")

if __name__ == "__main__":
    main() 