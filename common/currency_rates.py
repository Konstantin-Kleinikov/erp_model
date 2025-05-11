import xml.etree.ElementTree as ET
from datetime import date, datetime

import requests

from common.models import Currency, CurrencyRate


def download_currency_rates(user, date_req=None):
    """Fetch currency rates from the Central Bank of Russia."""
    date_req = date_req or date.today().strftime('%d/%m/%Y')
    url = ("http://www.cbr.ru/scripts/XML_daily.asp?date_req="
           f"{date_req}"
           )

    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        rate_date = datetime.strptime(date_req, '%d/%m/%Y').date()
        existing_rates = set(CurrencyRate.objects
                             .filter(rate_date=rate_date)
                             .values_list('currency__code', flat=True)
                             )
        currencies = {c.code: c for c in Currency.objects.all()}

        rates = []
        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = float(currency.find('Value').text.replace(',', '.'))
            nominal = int(currency.find('Nominal').text)
            if code in currencies and code not in existing_rates:
                CurrencyRate.objects.create(
                    currency=currencies[code],
                    rate_date=rate_date,
                    nominal=nominal,
                    rate=value,
                    created_by=user,
                )
                rates.append(
                    {'code': code, 'value': value, 'nominal': nominal}
                )
        return rates
    except (requests.RequestException, ET.ParseError) as e:
        print(f"Error: {e}")
        return []
