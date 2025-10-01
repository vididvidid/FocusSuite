# FocusSuite - Beginner's Quick Start Guide

Welcome to FocusSuite! This guide will help you get started quickly, even if you're new to programming.

## What is FocusSuite?

FocusSuite is a smart desktop app that helps you stay focused by:
1. **Blocking distractions** on your screen in real-time
2. **Editing videos** to blur specific objects automatically

Think of it as a digital assistant that watches your screen and hides anything that might distract you from your work!

## Before You Start

You'll need:
- A Windows computer (Windows 10 or 11)
- About 30 minutes for setup
- An internet connection

## Step-by-Step Setup

### Step 1: Install Python 🐍

Python is the programming language FocusSuite is built with.

1. Go to [python.org](https://www.python.org/downloads/)
2. Click "Download Python 3.11.x" (the big yellow button)
3. Run the downloaded file
4. **IMPORTANT**: Check the box "Add Python to PATH" before clicking Install
5. Click "Install Now"

**Test it worked:**
- Press `Windows + R`, type `cmd`, press Enter
- Type `python --version` and press Enter
- You should see something like "Python 3.11.x"

### Step 2: Install Tesseract (Text Recognition) 👁️

This helps FocusSuite read text from your screen.

**Easy way (recommended):**
1. Download from [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/releases)
2. Get the latest `tesseract-ocr-w64-setup-v5.x.x.exe` file
3. Run it and install with default settings

**Alternative way:**
1. Install [Chocolatey](https://chocolatey.org/install) (a Windows package manager)
2. Open Command Prompt as Administrator
3. Type: `choco install tesseract`

### Step 3: Download FocusSuite 📥

1. Go to the [FocusSuite GitHub page](https://github.com/jassu2244/FocusSuite)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop (or wherever you want)

### Step 4: Install FocusSuite Dependencies 📦

1. Press `Windows + R`, type `cmd`, press Enter
2. Navigate to the FocusSuite folder:
   ```
   cd Desktop\FocusSuite-main
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   
This will take a few minutes and install all the tools FocusSuite needs.

### Step 5: Get an OpenAI API Key (Optional but Recommended) 🔑

For the best experience, you'll need an OpenAI API key:

1. Go to [OpenAI's website](https://platform.openai.com/api-keys)
2. Sign up for an account (you'll need to verify your phone number)
3. Click "Create new secret key"
4. Copy the key (it starts with "sk-")
5. **Keep this key safe and don't share it!**

**Cost:** Usually $0.01-$0.05 per hour of use (very cheap!)

### Step 6: Run FocusSuite! 🚀

1. In your command prompt (still in the FocusSuite folder), type:
   ```
   python FocusSuite/main.py
   ```
2. The FocusSuite window should open!

## First Time Setup

### Configure Your API Key
1. Click the "Settings" tab
2. Paste your OpenAI API key in the "API Key" field
3. Click "Test Connection" to make sure it works
4. You should see "Connection successful!"

### Set Up Focus Monitoring
1. Click the "Distraction Blocker" tab
2. In the "Focus Topic" field, type what you want to focus on (e.g., "writing my essay")
3. Make sure "OpenAI" is selected as the provider
4. Click "Start Monitoring"

Now FocusSuite will watch your screen and blur any text that might distract you from your focus topic!

## Your First Test

Let's test if everything works:

1. Start monitoring with focus topic "work tasks"
2. Open a web browser
3. Go to a news website or social media
4. You should see black boxes covering distracting content!
5. Click "Stop Monitoring" when done

## Common Beginner Issues

### "python is not recognized as a command"
- You need to install Python and add it to PATH (see Step 1)
- Restart your computer after installing Python

### "Tesseract not found"
- Make sure you installed Tesseract OCR (see Step 2)
- Check that the path in `FocusSuite/utils/constants.py` is correct

### "API key invalid"
- Make sure you copied the full API key from OpenAI
- The key should start with "sk-"
- Check for extra spaces when pasting

### High CPU usage
- This is normal when monitoring is active
- The app analyzes your screen in real-time
- Close other heavy applications if needed

## What Each Tab Does

### Distraction Blocker Tab
- **Focus Topic**: What you want to focus on
- **Provider**: Choose OpenAI (recommended) or local worker
- **Start/Stop**: Control the monitoring
- **Console**: Shows what the app is doing

### Focus Video Tab
- **Select Video**: Choose a video file to edit
- **Blur Prompt**: Describe what to blur ("faces", "license plates", etc.)
- **Start Processing**: Begin the AI video editing

### Settings Tab
- **API Key**: Your OpenAI key
- **Worker URL**: For advanced users with local AI
- **Whitelist**: Apps that won't trigger monitoring
- **Theme**: Change the app's appearance

## Tips for Beginners

### Good Focus Topics
- Be specific: "writing my report" instead of "work"
- Use your language: "studying Python programming"
- Context helps: "preparing for my presentation"

### Video Blur Prompts
- Simple works best: "blur faces"
- Be descriptive: "hide all license plates"
- Test with short videos first

### Performance Tips
- Close unnecessary programs while monitoring
- Use shorter focus sessions (1-2 hours)
- Test settings with simple websites first

## Need More Help?

### Learning Resources
- [Python Basics Tutorial](https://www.python.org/about/gettingstarted/)
- [Complete Documentation](DOCUMENTATION.md) (for advanced users)
- [GitHub Issues](https://github.com/jassu2244/FocusSuite/issues) (report problems)

### Community
- Ask questions in GitHub Discussions
- Read the FAQ in the full documentation
- Check existing issues for solutions

## Next Steps

Once you're comfortable with the basics:
1. Try different AI providers
2. Experiment with custom themes
3. Set up application whitelists
4. Process some videos
5. Read the full documentation to understand how it works

## Safety Notes

- **Never share your API key** with anyone
- **Start with short monitoring sessions** to test performance
- **Keep backups** of important videos before processing
- **Monitor your OpenAI usage** to avoid unexpected charges

---

**Congratulations!** You now have FocusSuite running and helping you stay focused. Remember, it takes a few tries to get everything working perfectly - that's totally normal!

**Ready for more?** Check out the [complete documentation](DOCUMENTATION.md) to learn about advanced features and how the code works.

---

*Need help? Open an issue on GitHub or check the troubleshooting section in the full documentation.*