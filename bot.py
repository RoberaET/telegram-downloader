import os
import asyncio
import logging
import requests
import json
from typing import Optional
from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Try to import config for local development, fallback to environment variables
try:
    import config
    TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
    MAX_FILE_SIZE = config.MAX_FILE_SIZE
    DOWNLOAD_TIMEOUT = config.DOWNLOAD_TIMEOUT
    RAPIDAPI_KEY = getattr(config, 'RAPIDAPI_KEY', 'c0fe76b43emsh3180b8539e2afaep11551fjsn7990c143c224')
except ImportError:
    # Use environment variables for deployment
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB default
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 300))  # 5 minutes default
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', 'c0fe76b43emsh3180b8539e2afaep11551fjsn7990c143c224')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TikTokDownloader:
    def __init__(self):
        self.max_file_size = MAX_FILE_SIZE
        self.download_timeout = DOWNLOAD_TIMEOUT
        self.api_key = RAPIDAPI_KEY
        self.api_host = "tiktok-video-downloader-api.p.rapidapi.com"
        
    def is_tiktok_url(self, url: str) -> bool:
        """Check if the URL is a TikTok URL"""
        parsed = urlparse(url)
        return any(domain in parsed.netloc.lower() for domain in ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com'])
    
    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video information using RapidAPI"""
        try:
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': self.api_host
            }
            
            params = {
                'videoUrl': url
            }
            
            response = requests.get(
                f"https://{self.api_host}/media",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"API Response: {data}")
                return data
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def download_video(self, url: str, output_path: str) -> Optional[str]:
        """Download TikTok video using RapidAPI"""
        try:
            # First get video info
            video_info = self.get_video_info(url)
            if not video_info:
                logger.error("Could not get video info from API")
                return None
            
            # Extract video URL from API response
            video_url = None
            
            # Try different possible response formats
            if isinstance(video_info, dict):
                # Check for direct video URL
                if 'video' in video_info and isinstance(video_info['video'], list) and len(video_info['video']) > 0:
                    video_url = video_info['video'][0].get('url')
                elif 'video' in video_info and isinstance(video_info['video'], dict):
                    video_url = video_info['video'].get('url')
                elif 'url' in video_info:
                    video_url = video_info['url']
                elif 'data' in video_info and isinstance(video_info['data'], dict):
                    data = video_info['data']
                    if 'video' in data and isinstance(data['video'], list) and len(data['video']) > 0:
                        video_url = data['video'][0].get('url')
                    elif 'url' in data:
                        video_url = data['url']
            
            if not video_url:
                logger.error(f"No video URL found in API response: {video_info}")
                return None
            
            logger.info(f"Downloading video from: {video_url}")
            
            # Download the video
            response = requests.get(video_url, timeout=60, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Check file size
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    if file_size > self.max_file_size:
                        os.remove(output_path)
                        logger.error(f"File too large: {file_size} bytes")
                        return None
                    logger.info(f"Successfully downloaded: {output_path} ({file_size} bytes)")
                    return output_path
                else:
                    logger.error(f"Download completed but file not found: {output_path}")
                    return None
            else:
                logger.error(f"Failed to download video: {response.status_code}")
                return None
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables or config file")
        
        self.downloader = TikTokDownloader()
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎵 Welcome to TikTok Video Downloader Bot! 🎵

I can help you download TikTok videos without watermarks using RapidAPI.

📱 Just send me a TikTok video URL and I'll download it for you!

Commands:
/start - Show this welcome message
/help - Show help information

⚠️ Note: Please respect copyright and only download videos you have permission to use.
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 How to use", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📖 How to use TikTok Downloader Bot:

1️⃣ Copy a TikTok video URL from the TikTok app or website
2️⃣ Send the URL to this bot
3️⃣ Wait for the bot to process and download the video
4️⃣ Receive your downloaded video without watermark!

🔗 Supported URL formats:
• https://www.tiktok.com/@username/video/1234567890
• https://vm.tiktok.com/xxxxx/
• https://vt.tiktok.com/xxxxx/

⚡ Powered by RapidAPI TikTok Video Downloader

⚠️ Important notes:
• Maximum file size: 50MB
• Download time depends on video size and your internet speed
• Only public TikTok videos can be downloaded
• Respect copyright and fair use policies

Need help? Contact the bot administrator.
        """
        
        await update.message.reply_text(help_message)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages with TikTok URLs"""
        message_text = update.message.text.strip()
        
        # Check if message contains a TikTok URL
        if not self.downloader.is_tiktok_url(message_text):
            await update.message.reply_text(
                "❌ Please send a valid TikTok video URL.\n\n"
                "Example: https://www.tiktok.com/@username/video/1234567890"
            )
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text("🔄 Processing your TikTok video with RapidAPI...")
        
        try:
            # Create output filename
            video_id = f"tiktok_{hash(message_text) % 1000000}"
            output_filename = f"tiktok_{video_id}.mp4"
            
            # Download the video
            await processing_msg.edit_text("⬇️ Downloading video...")
            
            # Run download in executor to avoid blocking
            loop = asyncio.get_event_loop()
            downloaded_path = await loop.run_in_executor(
                None, 
                self.downloader.download_video, 
                message_text, 
                output_filename
            )
            
            if not downloaded_path:
                await processing_msg.edit_text(
                    "❌ Failed to download video.\n\n"
                    "Possible reasons:\n"
                    "• Video is private or deleted\n"
                    "• RapidAPI service is temporarily unavailable\n"
                    "• Video is region-restricted\n"
                    "• URL format is not supported\n\n"
                    "Please try:\n"
                    "• Using a different TikTok video\n"
                    "• Checking if the video is public\n"
                    "• Waiting a few minutes and trying again"
                )
                return
            
            # Send the video
            await processing_msg.edit_text("📤 Sending video...")
            
            with open(downloaded_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"🎵 Downloaded TikTok Video\n\n"
                           f"Original URL: {message_text}\n"
                           f"Downloaded by @{context.bot.username}\n"
                           f"⚡ Powered by RapidAPI"
                )
            
            # Clean up downloaded file
            os.remove(downloaded_path)
            await processing_msg.delete()
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            await processing_msg.edit_text("❌ An error occurred while processing the video. Please try again later.")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline keyboards"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            await self.help_command(update, context)
    
    def run(self):
        """Start the bot"""
        logger.info("Starting TikTok Downloader Bot with RapidAPI...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error: {e}")
        print("Please check your TELEGRAM_BOT_TOKEN in environment variables or config.py file")

if __name__ == "__main__":
    main() 