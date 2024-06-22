import os
import logging
from dotenv import load_dotenv
from bot.bot import TelegramBot
from bot.audio import Audio

load_dotenv()

# resetar pasta de audio
Audio(name='clear').clear_audio_directory()

log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

TELEBOT_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o bot do Telegram
telegram_bot = TelegramBot(api_key=TELEBOT_API_KEY, openai_api_key=OPENAI_API_KEY, logger=logging.getLogger(__name__))
telegram_bot.start_bot()
telegram_bot.run()