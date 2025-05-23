import os
from datetime import datetime

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
    """
    Handles the /download_rates command in the Telegram bot.

    This function allows users to download currency rates for a specific date
    or the current date if no date is provided. The date must be in the format
    YYYY-MM-DD. If the Telegram chat_id is not linked with user, an error message
    is sent.

    Args:
        message (types.Message): The Telegram message object containing the command
        and optional date argument.

    Behavior:
        - Extracts the user's Telegram ID from the message.
        - Retrieves the corresponding TelegramUser from the database.
        - Parses the date argument if provided, ensuring it is in the correct format.
        - Calls the `download_currency_rates` function to download rates for the user.
        - Sends appropriate success or error messages back to the user.

    Exceptions:
        - TelegramUser.DoesNotExist: If the user is not found in the database.
        - ValueError: If the provided date is in an invalid format.
        - Exception: For any other unexpected errors.
    """
    chat_id = message.chat.id
    try:
        telegram_user = TelegramUser.objects.get(telegram_id=chat_id)
        command_parts = message.text.split()
        date_req = None  # If no date is provided, download for the current date

        if len(command_parts) > 1:
            try:
                date_req = datetime.strptime(command_parts[1], '%Y-%m-%d').strftime('%d/%m/%Y')  # Parse date string
            except ValueError:
                bot.send_message(chat_id, "Invalid date format. Please use YYYY-MM-DD.")
                return

        bot.send_message(chat_id, "Downloading currency rates...")
        rates = download_currency_rates(telegram_user.user, date_req)
        bot.send_message(chat_id, "Rates downloaded successfully." if rates else "No rates were downloaded.")
    except TelegramUser.DoesNotExist:
        bot.send_message(chat_id, "User linked to Telegram not found.")
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
