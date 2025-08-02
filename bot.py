import os
import asyncio
import logging
from typing import Optional
from urllib.parse import urlparse
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TikTokDownloader:
    def __init__(self):
        self.max_file_size = config.MAX_FILE_SIZE  # 50MB default
        self.download_timeout = config.DOWNLOAD_TIMEOUT  # 5 minutes default
        
    def is_tiktok_url(self, url: str) -> bool:
        """Check if the URL is a TikTok URL"""
        parsed = urlparse(url)
        return any(domain in parsed.netloc.lower() for domain in ['tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com'])
    
    def get_video_info(self, url: str) -> Optional[dict]:
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def download_video(self, url: str, output_path: str) -> Optional[str]:
        """Download TikTok video"""
        try:
            ydl_opts = {
                'format': 'best[filesize<50M]/best',
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Check if file was downloaded
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                if file_size > self.max_file_size:
                    os.remove(output_path)
                    return None
                return output_path
            return None
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None

class TelegramBot:
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in config file")
        
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

I can help you download TikTok videos without watermarks.

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
        processing_msg = await update.message.reply_text("🔄 Processing your TikTok video...")
        
        try:
            # Get video info first
            video_info = self.downloader.get_video_info(message_text)
            if not video_info:
                await processing_msg.edit_text("❌ Could not fetch video information. Please check the URL and try again.")
                return
            
            # Create output filename
            video_id = video_info.get('id', 'unknown')
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
                await processing_msg.edit_text("❌ Failed to download video. The video might be private or unavailable.")
                return
            
            # Send the video
            await processing_msg.edit_text("📤 Sending video...")
            
            with open(downloaded_path, 'rb') as video_file:
                await update.message.reply_video(
                    video=video_file,
                    caption=f"🎵 Downloaded TikTok Video\n\n"
                           f"Original URL: {message_text}\n"
                           f"Downloaded by @{context.bot.username}"
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
        logger.info("Starting TikTok Downloader Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error: {e}")
        print("Please check your TELEGRAM_BOT_TOKEN in the config.py file")

if __name__ == "__main__":
    main() 