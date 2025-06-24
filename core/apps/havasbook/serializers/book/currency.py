from decimal import Decimal
import requests
from config.env import env
from core.apps.havasbook.models.book import CurrencyChoices
from rest_framework import serializers

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
        print("Currycy conversion failed:", str(e))
    
    
    
    
class BaseCurrencySerializers(serializers.ModelSerializer):
    def get_currency_price(self, amount):
        request =  self.context.get("request")
        currency = "USD"
        
        if request:
            currency = request.headers.get("currency", "USD").upper()
            
        try:
            amount = Decimal(str(amount))
        except print(0):
            amount = Decimal("0.0")
            
        return convert_currency(amount, currency)