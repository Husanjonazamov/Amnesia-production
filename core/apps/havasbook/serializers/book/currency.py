from decimal import Decimal
import requests
from config.env import env
import logging


EXCHANGE_URL = env("EXCHANGE_URL")

def convert_currency(amount: Decimal, to_currency: str) -> Decimal:
    if to_currency == "USD":
        return round(amount, 2)

    try:
        url = EXCHANGE_URL
        response = requests.get(url, timeout=3)
        data = response.json()
        logging.error(f"--------\n\n{url}\n\n-----------")
        
        if data.get("result") != "success":
            print("Currency API failed")
            return round(amount, 2)

        rate = data.get("conversion_rates", {}).get(to_currency.upper())
        if rate is None:
            return round(amount, 2)

        return round(amount * Decimal(str(rate)), 2)
    
    except Exception as e:
        print("Currency conversion error:", e)
        return round(amount, 2)