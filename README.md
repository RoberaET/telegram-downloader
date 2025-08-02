# TikTok Video Downloader Telegram Bot

A powerful Telegram bot that downloads TikTok videos without watermarks. Built with Python and the `python-telegram-bot` library.

## Features

- 🎵 Download TikTok videos without watermarks
- 📱 User-friendly Telegram interface
- ⚡ Fast and efficient downloading
- 🔒 Automatic file size limits (50MB max)
- 🧹 Automatic cleanup of downloaded files
- 📊 Progress updates during download
- 🛡️ Error handling and user feedback

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Internet connection

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd telegram-downloader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**
   - Your bot token is already configured in `config.py`
   - If you need to change it, edit the `config.py` file:
   ```python
   TELEGRAM_BOT_TOKEN = "your_bot_token_here"
   ```

## Getting Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided by BotFather
5. Paste it in your `config.py` file

## Usage

1. **Start the bot**
   ```bash
   python bot.py
   ```

2. **In Telegram**
   - Find your bot by the username you created
   - Send `/start` to begin
   - Send a TikTok video URL to download the video

## Supported URL Formats

- `https://www.tiktok.com/@username/video/1234567890`
- `https://vm.tiktok.com/xxxxx/`
- `https://vt.tiktok.com/xxxxx/`

## Configuration Options

You can customize the bot behavior by modifying the `config.py` file:

```python
# Telegram Bot Token (required)
TELEGRAM_BOT_TOKEN = "your_bot_token_here"

# Maximum file size for downloads (in bytes, default: 50MB)
MAX_FILE_SIZE = 52428800

# Download timeout (in seconds, default: 5 minutes)
DOWNLOAD_TIMEOUT = 300
```

## Bot Commands

- `/start` - Show welcome message and bot information
- `/help` - Display detailed usage instructions

## How It Works

1. **URL Validation**: The bot checks if the provided URL is a valid TikTok URL
2. **Video Info Extraction**: Uses `yt-dlp` to extract video information
3. **Download**: Downloads the video in the best available quality
4. **File Size Check**: Ensures the downloaded file doesn't exceed size limits
5. **Send to User**: Sends the video back to the user via Telegram
6. **Cleanup**: Automatically removes the downloaded file from the server

## Error Handling

The bot handles various error scenarios:
- Invalid TikTok URLs
- Private or unavailable videos
- Network connectivity issues
- File size limitations
- Download timeouts

## Legal and Ethical Considerations

⚠️ **Important**: This bot is for educational purposes and personal use only. Please:

- Respect copyright laws and intellectual property rights
- Only download videos you have permission to use
- Don't use downloaded content for commercial purposes without proper licensing
- Be mindful of TikTok's Terms of Service

## Troubleshooting

### Common Issues

1. **"TELEGRAM_BOT_TOKEN not found"**
   - Make sure you've configured your bot token in `config.py`
   - Check that the token is correct and not expired

2. **"Could not fetch video information"**
   - The video might be private or deleted
   - Check if the TikTok URL is valid and accessible
   - Try with a different TikTok video

3. **"Failed to download video"**
   - Network connectivity issues
   - TikTok might have changed their API
   - Video might be region-restricted

4. **"File too large"**
   - The video exceeds the 50MB limit
   - Consider downloading shorter videos

### Updating Dependencies

If you encounter issues, try updating the dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is for educational purposes. Please use responsibly and in accordance with applicable laws and terms of service.

## Support

If you need help or have questions:
1. Check the troubleshooting section above
2. Review the error messages in the console
3. Ensure all dependencies are properly installed
4. Verify your bot token is correct

---

**Note**: This bot uses `yt-dlp` which is regularly updated to handle changes in TikTok's API. If downloads stop working, consider updating `yt-dlp` to the latest version. 