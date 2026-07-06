# Samuel's Creative Bot 🤖

A feature-rich Telegram bot providing creative and utility tools for everyone.

## 🌟 Features

- **URL Shortener** - Shorten long URLs instantly
- **Word Counter** - Analyze text statistics
- **Plagiarism Checker** - Check text originality
- **Image Tools** - Conversion and generation (Coming Soon)

## 🚀 Quick Start

### Deploy on Railway

1. Click "New Project" → "Deploy from GitHub"
2. Connect your GitHub repository
3. Add environment variable:
   - `TELEGRAM_BOT_TOKEN` = your_bot_token
4. Deploy!

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/samuelcreative1bot.git

# Install dependencies
pip install -r requirements.txt

# Set environment variable (on Unix)
export TELEGRAM_BOT_TOKEN="your_bot_token"

# On Windows
set TELEGRAM_BOT_TOKEN="your_bot_token"

# Run the bot
python bot.py
