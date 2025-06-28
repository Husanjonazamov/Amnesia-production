# core/apps/havasbook/serializers/book/currency.py

from decimal import Decimal
import requests
from config.env import env
from core.apps.havasbook.models.book import CurrencyChoices

EXCHANGE_URL = env("EXCHANGE_URL")


def convert_currency(amount: Decimal, to_currency: str) -> Decimal:
    if to_currency.upper() == "USD":
        return round(amount, 2)

    try:
        response = requests.get(EXCHANGE_URL, timeout=3)
        data = response.json()

        # API javobi "rates" ni qaytaradi (emas "conversion_rates")
        if data.get("result") != "success":
            return round(amount, 2)

        rate = data.get("rates", {}).get(to_currency.upper())  
        if rate is None:
            return round(amount, 2)

        return round(amount * Decimal(str(rate)), 2)

    except Exception:
        return round(amount, 2)


class BaseCurrencyPriceMixin:
    def get_currency_price(self, amount):
        request = self.context.get("request")
        currency = request.headers.get("currency", "USD").upper() if request else "USD"

        try:
            amount = Decimal(str(amount))
        except:
            amount = Decimal("0.0")

        return convert_currency(amount, currency)
