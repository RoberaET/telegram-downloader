# 🚀 Telegram Bot Deployment Guide

This guide will help you deploy your TikTok downloader bot to run 24/7 on various hosting platforms.

## 📋 Prerequisites

- ✅ Your bot token: `8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg`
- ✅ Bot username: `@rotoktokdownloaderbot`
- ✅ All code files ready

## 🌐 Deployment Options

### Option 1: Railway (Recommended - Free)

**Railway** offers free hosting with automatic deployments from GitHub.

#### Steps:

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/telegram-downloader.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect Python and deploy

3. **Set Environment Variables**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add: `TELEGRAM_BOT_TOKEN = 8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg`

4. **Deploy**
   - Railway will automatically deploy your bot
   - Check the logs to ensure it's running

### Option 2: Render (Free)

**Render** offers free hosting with easy deployment.

#### Steps:

1. **Create a GitHub Repository** (same as above)

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python bot.py`
   - Add environment variable: `TELEGRAM_BOT_TOKEN = 8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg`

### Option 3: Heroku (Paid)

**Heroku** is a popular platform but requires a credit card for verification.

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-bot-name
   ```

3. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

4. **Set Environment Variable**
   ```bash
   heroku config:set TELEGRAM_BOT_TOKEN=8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg
   ```

### Option 4: DigitalOcean App Platform

**DigitalOcean** offers reliable hosting with a free tier.

#### Steps:

1. **Create GitHub Repository** (same as above)

2. **Deploy to DigitalOcean**
   - Go to [digitalocean.com](https://digitalocean.com)
   - Create account
   - Go to "Apps" → "Create App"
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `python bot.py`
   - Add environment variable: `TELEGRAM_BOT_TOKEN = 8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg`

## 🔧 Local Development

For local development, use the virtual environment:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## 📱 Testing Your Deployed Bot

1. **Find your bot**: https://t.me/rotoktokdownloaderbot
2. **Send `/start`** to begin
3. **Send a TikTok URL** to test downloading
4. **Check logs** in your hosting platform dashboard

## 🔍 Troubleshooting

### Common Issues:

1. **Bot not responding**
   - Check if the bot is running in your hosting platform
   - Verify the bot token is correct
   - Check the logs for errors

2. **Import errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check if the hosting platform supports your Python version

3. **Download failures**
   - TikTok may have changed their API
   - Update yt-dlp: `pip install --upgrade yt-dlp`

### Monitoring:

- **Railway**: Check the "Deployments" tab for logs
- **Render**: Check the "Logs" tab
- **Heroku**: Use `heroku logs --tail`
- **DigitalOcean**: Check the "Logs" section

## 🎯 Recommended Deployment

**For beginners**: Use **Railway** - it's free, easy to set up, and reliable.

**For production**: Use **DigitalOcean** or **Heroku** for better performance and support.

## 📞 Support

If you encounter issues:
1. Check the hosting platform's documentation
2. Review the error logs
3. Ensure your bot token is valid
4. Test locally first

---

**Your bot is ready to deploy!** 🚀 