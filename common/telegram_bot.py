import os

import django
from dotenv import load_dotenv
from telebot import TeleBot, types

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_model.settings')
django.setup()

from common.currency_rates import download_currency_rates
from common.models import TelegramUser

# Load environment variables
load_dotenv()
bot = TeleBot(token=os.getenv('YOUR_TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['download_rates'])
def download_rates_command(message: types.Message):
    chat_id = message.chat.id
    telegram_user = TelegramUser.objects.get(telegram_id=chat_id)  # TODO get_object_or_404()
    bot.send_message(chat_id, "Downloading currency rates...")
    try:
        rates = download_currency_rates(telegram_user.user)
        msg = "Rates downloaded successfully." if rates else "No rates were downloaded."
        bot.send_message(chat_id, msg)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")


@bot.message_handler(commands=['start'])
def wake_up(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('/start'),
        types.KeyboardButton('/download_rates'),
    )

    bot.send_message(
        message.chat.id,
        f"Hello, {message.chat.first_name}! Use the button below to download rates.",
        reply_markup=keyboard,
    )


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
