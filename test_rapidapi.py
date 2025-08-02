#!/usr/bin/env python3
"""
Test script for RapidAPI TikTok Video Downloader
"""

import requests
import json
import sys

def test_rapidapi_download(url):
    """Test downloading a TikTok video using RapidAPI"""
    print(f"🧪 Testing RapidAPI download for: {url}")
    
    api_key = "c0fe76b43emsh3180b8539e2afaep11551fjsn7990c143c224"
    api_host = "tiktok-video-downloader-api.p.rapidapi.com"
    
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': api_host
    }
    
    params = {
        'videoUrl': url
    }
    
    print("\n1. Testing API connection...")
    try:
        response = requests.get(
            f"https://{api_host}/media",
            headers=headers,
            params=params,
            timeout=30
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Response received!")
            print(f"   📊 Response data: {json.dumps(data, indent=2)}")
            
            # Try to extract video URL
            video_url = None
            if isinstance(data, dict):
                if 'video' in data and isinstance(data['video'], list) and len(data['video']) > 0:
                    video_url = data['video'][0].get('url')
                elif 'video' in data and isinstance(data['video'], dict):
                    video_url = data['video'].get('url')
                elif 'url' in data:
                    video_url = data['url']
                elif 'data' in data and isinstance(data['data'], dict):
                    data_inner = data['data']
                    if 'video' in data_inner and isinstance(data_inner['video'], list) and len(data_inner['video']) > 0:
                        video_url = data_inner['video'][0].get('url')
                    elif 'url' in data_inner:
                        video_url = data_inner['url']
            
            if video_url:
                print(f"   🎥 Video URL found: {video_url}")
                return True
            else:
                print(f"   ❌ No video URL found in response")
                return False
        else:
            print(f"   ❌ API Error: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 RapidAPI TikTok Downloader Test")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter TikTok URL to test: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    success = test_rapidapi_download(url)
    
    if success:
        print("\n🎉 RapidAPI test completed successfully!")
        print("Your bot should work with this API.")
    else:
        print("\n❌ RapidAPI test failed!")
        print("This might be due to:")
        print("• Invalid API key")
        print("• Private video")
        print("• API rate limits")
        print("• Network issues")

if __name__ == "__main__":
    main() 