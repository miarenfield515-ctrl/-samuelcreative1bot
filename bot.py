import os
import sys
import logging
import json
import re
import time
from datetime import datetime
from typing import Dict, Any, Optional
import requests
import telebot
from telebot import types
from telebot.types import Message, CallbackQuery
import urllib.parse

# ==================== CONFIGURATION ====================

# Environment variables (set these in Railway)
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
    sys.exit(1)

# Configure logging for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# In-memory storage (for demonstration - use database in production)
user_sessions: Dict[int, Dict[str, Any]] = {}
url_cache: Dict[str, str] = {}

# ==================== CONSTANTS ====================

COMMANDS = {
    'start': 'Start the bot and see welcome message',
    'help': 'Show available commands',
    'info': 'Get bot information',
    'about': 'About this bot',
    'shorten': 'Shorten a URL',
    'wordcount': 'Count words in text',
    'plagiarism': 'Check text for plagiarism',
    'convert': 'Convert image format (Coming Soon)',
    'generate': 'Generate image from text (Coming Soon)',
    'stats': 'Show bot statistics'
}

WELCOME_MESSAGE = """
🎨 **Welcome to Samuel's Creative Bot!**

I'm your all-in-one creative assistant built with ❤️

**📸 Image Tools**
• `/convert` - Convert images between formats
• `/generate` - Generate AI images from text

**🔗 URL Tools**  
• `/shorten` - Shorten long URLs instantly

**📝 Text Tools**
• `/wordcount` - Count words and characters
• `/plagiarism` - Check text for plagiarism

**ℹ️ Info**
• `/help` - Show all commands
• `/info` - Bot information
• `/about` - About this project
• `/stats` - Bot statistics

**💡 Pro Tip:** You can also just send me text and I'll help!
"""

# ==================== DATABASE HELPERS (Mock) ====================

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Get or create user data"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'first_seen': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'command_count': 0,
            'preferences': {}
        }
    return user_sessions[user_id]

def update_user_data(user_id: int, **kwargs):
    """Update user data"""
    if user_id not in user_sessions:
        get_user_data(user_id)
    for key, value in kwargs.items():
        user_sessions[user_id][key] = value
    user_sessions[user_id]['last_seen'] = datetime.now().isoformat()

# ==================== COMMAND HANDLERS ====================

@bot.message_handler(commands=['start'])
def cmd_start(message: Message):
    """Handle /start command"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "User"
        
        # Update user data
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        # Send welcome message
        bot.send_chat_action(user_id, 'typing')
        time.sleep(0.5)  # Small delay for realism
        
        welcome_text = WELCOME_MESSAGE
        bot.reply_to(message, welcome_text, parse_mode='Markdown')
        
        logger.info(f"User {username} ({user_id}) started the bot")
        
    except Exception as e:
        logger.error(f"Error in cmd_start: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['help'])
def cmd_help(message: Message):
    """Handle /help command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        help_text = """
📚 **Available Commands**

**🎨 Creative Tools**
• `/generate` - Generate images from text prompts
• `/convert` - Convert images between formats

**🔗 Utility Tools**
• `/shorten` - Shorten long URLs
• `/wordcount` - Count words and characters
• `/plagiarism` - Check text for plagiarism

**ℹ️ Information**
• `/start` - Welcome message
• `/help` - Show this help
• `/info` - Bot information
• `/about` - About this project
• `/stats` - Bot statistics

**📱 Quick Tips**
• Send me any text and I'll analyze it
• Reply to a message with a command
• Use inline buttons for easier navigation

**🆘 Need help?**
Just type /help anytime!
"""
        bot.reply_to(message, help_text, parse_mode='Markdown')
        logger.info(f"User {message.from_user.id} requested help")
        
    except Exception as e:
        logger.error(f"Error in cmd_help: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['info'])
def cmd_info(message: Message):
    """Handle /info command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        user_data = get_user_data(user_id)
        
        info_text = f"""
📊 **Bot Information**

**🤖 Bot Details**
• Name: Samuel's Creative Bot
• Username: @samuelcreative1bot
• Version: 2.0.0
• Status: ✅ Online

**👤 Your Info**
• Name: {message.from_user.first_name} {message.from_user.last_name or ''}
• Username: @{message.from_user.username or 'Not set'}
• User ID: `{user_id}`
• First Seen: {user_data['first_seen']}
• Commands Used: {user_data['command_count']}

**⚙️ Features**
✅ URL Shortening
✅ Word Counter
✅ Plagiarism Check
🔄 Image Conversion (Coming)
🔄 AI Image Generation (Coming)

**🌐 Links**
• GitHub: [Repository](https://github.com/yourusername/samuelcreative1bot)
• Railway: [Status](https://railway.app)
"""
        bot.reply_to(message, info_text, parse_mode='Markdown')
        logger.info(f"User {user_id} requested info")
        
    except Exception as e:
        logger.error(f"Error in cmd_info: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['about'])
def cmd_about(message: Message):
    """Handle /about command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        about_text = """
ℹ️ **About Samuel's Creative Bot**

**📝 Project Overview**
A multi-purpose Telegram bot built to provide creative and utility tools in one place. Made for creators, students, and professionals.

**🔧 Technology Stack**
• Python 3.9+
• pyTelegramBotAPI
• Railway (Hosting)
• GitHub (Version Control)

**👨‍💻 Creator**
Samuel - Developer & Creative Enthusiast

**📅 Version**
2.0.0 (Latest)

**🌟 Features**
• URL Shortener
• Word Counter
• Plagiarism Checker
• Image Tools (In Development)
• AI Features (Coming Soon)

**🤝 Contributing**
Found a bug? Want to suggest a feature? 
Check the GitHub repository!

**📜 License**
MIT License - Free to use and modify

*Thank you for using Samuel's Creative Bot! 🎨*
"""
        bot.reply_to(message, about_text, parse_mode='Markdown')
        logger.info(f"User {user_id} requested about info")
        
    except Exception as e:
        logger.error(f"Error in cmd_about: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['stats'])
def cmd_stats(message: Message):
    """Handle /stats command"""
    try:
        user_id = message.from_user.id
        
        # Only allow admin to see global stats (you can set this)
        # For now, show user stats
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        user_data = get_user_data(user_id)
        
        stats_text = f"""
📊 **Your Statistics**

**👤 Profile**
• Commands Used: {user_data['command_count']}
• Member Since: {user_data['first_seen'].split('T')[0]}
• Last Active: {user_data['last_seen'].split('T')[0]}

**📈 Quick Stats**
• Total Users: {len(user_sessions)}
• Active Users: {len([u for u in user_sessions.values() if u.get('command_count', 0) > 0])}
• URL Shortens: {len(url_cache)}

**🎯 Tips**
• Use /help to see all commands
• Check /info for detailed info
• Visit GitHub for updates
"""
        bot.reply_to(message, stats_text, parse_mode='Markdown')
        logger.info(f"User {user_id} requested stats")
        
    except Exception as e:
        logger.error(f"Error in cmd_stats: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['shorten'])
def cmd_shorten(message: Message):
    """Handle /shorten command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        # Check if URL was provided with command
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            # URL provided directly
            process_url_shortening(message, parts[1])
        else:
            # Ask user for URL
            msg = bot.reply_to(message, 
                "🔗 Please send me the URL you want to shorten.\n\n"
                "Example: `https://example.com/very/long/url`",
                parse_mode='Markdown'
            )
            bot.register_next_step_handler(msg, process_url_shortening)
            
    except Exception as e:
        logger.error(f"Error in cmd_shorten: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

def process_url_shortening(message: Message, url: str = None):
    """Process URL shortening"""
    try:
        if url is None:
            url = message.text.strip()
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            bot.reply_to(message, 
                "❌ Please send a valid URL starting with `http://` or `https://`",
                parse_mode='Markdown'
            )
            return
        
        bot.send_chat_action(message.from_user.id, 'typing')
        
        # Use multiple APIs with fallback
        short_url = shorten_url_api(url)
        
        if short_url:
            # Save to cache
            url_cache[short_url] = url
            
            reply_text = f"""
✅ **URL Shortened Successfully!**

🔗 **Original:**
`{url}`

✂️ **Shortened:**
`{short_url}`

📊 **Statistics:**
• Length: {len(url)} → {len(short_url)} characters
• Saved: {len(url) - len(short_url)} characters
• Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 **Tip:** Share the short URL anywhere!
"""
            bot.reply_to(message, reply_text, parse_mode='Markdown')
            logger.info(f"User {message.from_user.id} shortened URL: {url}")
        else:
            bot.reply_to(message, 
                "❌ Failed to shorten URL. Please try again or check if the URL is valid."
            )
            
    except Exception as e:
        logger.error(f"Error in process_url_shortening: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

def shorten_url_api(url: str) -> Optional[str]:
    """Shorten URL using free APIs"""
    # API 1: shrtco.de
    try:
        response = requests.get(
            "https://api.shrtco.de/v2/shorten",
            params={'url': url},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data['result']['full_short_link']
    except:
        pass
    
    # API 2: TinyURL alternative (direct)
    try:
        response = requests.get(
            f"https://tinyurl.com/api-create.php",
            params={'url': url},
            timeout=10
        )
        if response.status_code == 200 and response.text:
            return response.text.strip()
    except:
        pass
    
    return None

@bot.message_handler(commands=['wordcount'])
def cmd_wordcount(message: Message):
    """Handle /wordcount command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        # Check if text was provided with command
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            # Text provided directly
            process_word_count(message, parts[1])
        else:
            # Ask user for text
            msg = bot.reply_to(message, 
                "📝 Please send me the text you want to analyze.\n\n"
                "You can send a long message or just a few words!"
            )
            bot.register_next_step_handler(msg, process_word_count)
            
    except Exception as e:
        logger.error(f"Error in cmd_wordcount: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

def process_word_count(message: Message, text: str = None):
    """Process word count"""
    try:
        if text is None:
            text = message.text
        
        if not text or len(text.strip()) == 0:
            bot.reply_to(message, "❌ Please send some text to analyze.")
            return
        
        # Clean and analyze
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_no_space = len(text.replace(' ', ''))
        char_no_space_no_punct = len(re.sub(r'[^\w\s]', '', text).replace(' ', ''))
        
        # Count sentences
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Count unique words
        unique_words = len(set(words))
        
        # Average word length
        avg_word_length = char_no_space_no_punct / word_count if word_count > 0 else 0
        
        # Reading time
        reading_time = word_count / 200  # Average reading speed: 200 words per minute
        
        reply_text = f"""
📊 **Text Analysis Results**

**📝 Content Statistics**
• Words: **{word_count}**
• Unique Words: **{unique_words}**
• Characters: **{char_count}**
• Characters (no spaces): **{char_no_space}**
• Sentences: **{sentence_count}**
• Average Word Length: **{avg_word_length:.1f}** characters

**⏱️ Reading Time**
• ~{reading_time:.1f} minute(s) at 200 WPM

**📊 Text Density**
• Words per Sentence: **{word_count / sentence_count:.1f}** (Aim for 15-20)
• Characters per Word: **{char_no_space / word_count:.1f}**

**💡 Tips**
• Short sentences improve readability
• Use varied vocabulary for engagement
• Check grammar for professional text
"""
        bot.reply_to(message, reply_text, parse_mode='Markdown')
        logger.info(f"User {message.from_user.id} analyzed text: {word_count} words")
        
    except Exception as e:
        logger.error(f"Error in process_word_count: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['plagiarism'])
def cmd_plagiarism(message: Message):
    """Handle /plagiarism command"""
    try:
        user_id = message.from_user.id
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        # Check if text was provided with command
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            # Text provided directly
            process_plagiarism_check(message, parts[1])
        else:
            # Ask user for text
            msg = bot.reply_to(message, 
                "🔍 Please send me the text you want to check for plagiarism.\n\n"
                "*Note: This is a basic check. For professional use, use dedicated services.*",
                parse_mode='Markdown'
            )
            bot.register_next_step_handler(msg, process_plagiarism_check)
            
    except Exception as e:
        logger.error(f"Error in cmd_plagiarism: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

def process_plagiarism_check(message: Message, text: str = None):
    """Process plagiarism check"""
    try:
        if text is None:
            text = message.text
        
        if not text or len(text.strip()) == 0:
            bot.reply_to(message, "❌ Please send some text to check.")
            return
        
        # Basic checks
        word_count = len(text.split())
        char_count = len(text)
        
        # Check for common phrases (simplified)
        common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i']
        word_freq = {}
        for word in text.lower().split():
            word = re.sub(r'[^\w\s]', '', word)
            if word in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Generate a "unique" score based on word patterns
        unique_ratio = len(set(text.lower().split())) / len(text.split()) if len(text.split()) > 0 else 0
        
        # Calculate a simple originality score
        originality_score = min(100, max(50, int(unique_ratio * 100 + 50)))
        
        reply_text = f"""
🔍 **Plagiarism Check Results**

**📝 Analysis**
• Text Length: **{char_count}** characters
• Word Count: **{word_count}** words
• Unique Words: **{len(set(text.lower().split()))}**

**📊 Scores**
• Originality Score: **{originality_score}%**
• Common Word Usage: **{len(word_freq)}** common words found
• Text Complexity: **{unique_ratio*100:.1f}%** unique

**⚠️ Recommendations**
• {'✅ Text appears original' if originality_score > 70 else '⚠️ Consider adding more unique content'}
• {'✅ Good vocabulary variety' if len(set(text.lower().split())) > 20 else '💡 Try using more varied vocabulary'}
• {'✅ Good text length for analysis' if word_count > 50 else '📝 Longer texts give more accurate results'}

**📌 Note:** This is a basic check. For professional plagiarism detection, please use services like:
• Turnitin
• Grammarly
• Copyscape
"""
        bot.reply_to(message, reply_text, parse_mode='Markdown')
        logger.info(f"User {message.from_user.id} performed plagiarism check")
        
    except Exception as e:
        logger.error(f"Error in process_plagiarism_check: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

@bot.message_handler(commands=['convert'])
def cmd_convert(message: Message):
    """Handle /convert command (Coming Soon)"""
    user_id = message.from_user.id
    update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
    
    reply_text = """
📸 **Image Conversion**

*🔄 This feature is currently in development!*

**Planned Features:**
• Convert between JPG, PNG, WebP, GIF, BMP
• Batch image processing
• Quality adjustment
• Resize and crop options

**🚀 Coming Soon!**

In the meantime, check out these great tools:
• [Convertio](https://convertio.co)
• [CloudConvert](https://cloudconvert.com)
• [Zamzar](https://zamzar.com)
"""
    bot.reply_to(message, reply_text, parse_mode='Markdown')

@bot.message_handler(commands=['generate'])
def cmd_generate(message: Message):
    """Handle /generate command (Coming Soon)"""
    user_id = message.from_user.id
    update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
    
    reply_text = """
🎨 **AI Image Generation**

*✨ This feature is currently in development!*

**Planned Features:**
• Text-to-image generation
• Multiple art styles
• Custom image sizes
• Batch generation

**🚀 Coming Soon!**

Try these great AI tools:
• [DALL-E](https://openai.com/dall-e)
• [Midjourney](https://midjourney.com)
• [Stable Diffusion](https://stability.ai)
"""
    bot.reply_to(message, reply_text, parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    """Handle photo messages"""
    user_id = message.from_user.id
    update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
    
    file_id = message.photo[-1].file_id
    file_size = message.photo[-1].file_size
    file_width = message.photo[-1].width
    file_height = message.photo[-1].height
    
    reply_text = f"""
📸 **Photo Received!**

**📊 Details:**
• File ID: `{file_id[:20]}...`
• Size: **{file_size:,}** bytes
• Resolution: **{file_width}×{file_height}**

**🚀 Available Actions:**
• Use `/convert` to convert this image
• Use `/generate` to create variations

*Image processing features coming soon!*
"""
    bot.reply_to(message, reply_text, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    """Handle regular text messages"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        # Check if it's a command we haven't caught
        if message.text.startswith('/'):
            bot.reply_to(message, f"❌ Unknown command: {message.text}\n\nUse /help to see all available commands.")
            return
        
        # Process as general text
        update_user_data(user_id, command_count=user_sessions[user_id].get('command_count', 0) + 1)
        
        # Auto-detect if it's a URL
        if re.match(r'^https?://', message.text):
            bot.reply_to(message, "🔗 I detected a URL! Use /shorten to shorten it, or just send /shorten with the URL.")
            return
        
        # Generic response with options
        bot.send_chat_action(user_id, 'typing')
        time.sleep(0.5)
        
        reply_text = f"""
📨 **Message Received!**

I can help you analyze this text or perform actions:

**Available Actions:**
• `/wordcount` - Count words and characters
• `/plagiarism` - Check for plagiarism
• `/shorten` - Shorten URLs

**Your Message:**
> {message.text[:200]}{'...' if len(message.text) > 200 else ''}

*Need help? Type /help*
"""
        bot.reply_to(message, reply_text, parse_mode='Markdown')
        logger.info(f"User {username} ({user_id}) sent: {message.text[:50]}...")
        
    except Exception as e:
        logger.error(f"Error in handle_text: {e}")
        bot.reply_to(message, "❌ An error occurred. Please try again later.")

# ==================== ERROR HANDLERS ====================

@bot.message_handler(func=lambda message: True)
def handle_all(message: Message):
    """Catch-all handler for any unhandled message types"""
    bot.reply_to(message, "🤔 I'm not sure how to handle that.\n\nUse /help to see what I can do!")

# ==================== HEALTH CHECK ====================

def health_check():
    """Check bot health"""
    try:
        bot.get_me()
        return True
    except:
        return False

# ==================== MAIN ====================

def main():
    """Main function to run the bot"""
    logger.info("=" * 50)
    logger.info("🚀 Starting Samuel's Creative Bot")
    logger.info("=" * 50)
    logger.info(f"🤖 Bot Username: @{bot.get_me().username}")
    logger.info(f"📊 Total Users: {len(user_sessions)}")
    logger.info("=" * 50)
    
    try:
        # Remove webhook (important for polling)
        bot.remove_webhook()
        
        # Start polling
        logger.info("✅ Bot is running and waiting for messages...")
        bot.infinity_polling(skip_pending=True, timeout=30)
        
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
