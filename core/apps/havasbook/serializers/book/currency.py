from decimal import Decimal
import requests
from config.env import env
from core.apps.havasbook.models.book import CurrencyChoices

EXCHANGE_URL = env("EXCHANGE_URL")



def convert_currency(amount: Decimal, to_currency: str):
    if to_currency == "USD":
        return round(amount, 2)

    try:
        url = EXCHANGE_URL
        response = requests.get(url, timeout=3)
        data = response.json()
        
        if data.get("result") != "success":
            return round(amount, 2)

        rate = data.get("conversion_rates", {}).get(to_currency.upper())
        if rate is None:
            return round(amount, 2)

        return round(amount * Decimal(str(rate)), 2)
    
    except Exception as e:
        return e
    
    
    
    
class CurrenCyPriceMixin:
    def get_currency_price(self, amount):
        print(f"====\n\n{amount}\n\n")
        result = {}
        
        for currency in CurrencyChoices.values:
            result[currency] =  convert_currency(amount, currency)
        
        return result