@echo off
echo ========================================
echo TikTok Downloader Bot Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download the latest Python version
    echo 3. Run the installer and check "Add Python to PATH"
    echo 4. Restart this script after installation
    echo.
    pause
    exit /b 1
)

echo Python is installed!
python --version
echo.

echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install packages. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Your bot is configured with token:
echo 8372261923:AAFlFNzdxvFBdzhNfOmBXmwDlm2W4Rozwfg
echo.
echo To start the bot, run:
echo python bot.py
echo.
echo To test the bot, run:
echo python test_bot.py
echo.
pause 