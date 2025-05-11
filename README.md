# ERP simple model
This project is currently being developed for the purpose of researching and analyzing the various 
patterns and techniques in Object-Oriented Programming via Python, that can be applied 
when creating a web application for a business area of enterprise resource planning (ERP). 

Additionally, the project should provide insight into the potential pros and cons of 
developing a business application using an object-oriented approach, as compared to 
the BaanC language used in the development of the ERP system Baan/LN.

## Project Overview
The functional scope of this model is limited by the following simplified business case:
* Generate master data required for: 
  * business partners (customers and suppliers) 
  * warehouses 
  * items (goods, materials).
* Generate some inventory transactions for item stock availability
* Create several sales orders with planned delivery dates
* Create a simple planning logic to calculate item stock availability at sales order delivery dates
* Generate purchase orders for non-available stock quantities, respecting suppliers lead time

The project is designed to demonstrate the use of Python's OOP capabilities in a business context.

## Features

- **Currency Management**:
  - Fetch and store currency rates from the Central Bank of Russia.
  - Manage currency rates and conversions for ERP documents.
- **Sales and Purchases**:
  - Create and manage sales and purchase orders.
  - Plan stock availability and generate purchase orders for shortages.
- **Integration with Telegram Bot**:
  - Use a Telegram bot to trigger currency rate downloads and interact with the system.

## Project Structure

### Master Data (`common`)
- **`Currency`**: Manage currency codes, names, and ISO standards.
- **`CurrencyRate`**: Store and manage exchange rates for currencies.
- **`TelegramUser`**: Link Telegram users to system users for bot interactions.

### Currency Rates (`common/currency_rates.py`)
- Fetch and store currency rates from external APIs.
- Avoid duplicate rates by checking existing records.

### Telegram Bot (`common/telegram_bot.py`)
- Interact with the ERP system using a Telegram bot.
- Commands include downloading currency rates and starting the bot.

### Sales (`sls`)
- Manage sales orders and calculate stock availability.

### Purchases (`pur`)
- Generate purchase orders based on stock shortages.

## Technologies Used

- **Python 3.13.0**
- **Django**: For ORM and database management.
- **Requests**: For API calls to fetch currency rates.
- **TeleBot**: For Telegram bot integration.
- **dotenv**: For managing environment variables.

## How to Run

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up the Django environment:
   - Configure the `DJANGO_SETTINGS_MODULE` environment variable.
   - Run migrations using `python manage.py migrate`.
4. Start the Telegram bot:
   - Set the `YOUR_TELEGRAM_BOT_TOKEN` in a `.env` file.
   - Run the bot using `python common/telegram_bot.py`.
5. Use the bot commands to interact with the system.

## Future Enhancements

- Add more ERP modules, such as invoicing and financial accounting.
- Improve planning logic for stock availability.
- Enhance the Telegram bot with additional commands and features.


## License

This project is for educational and research purposes. Feel free to explore and contribute.
