import requests
import json
from config import exchanges


usd = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
a = usd['Valute']['USD']['Value']

eur = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
b = eur['Valute']['EUR']['Value']


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/currency_data/convert?to={quote_key}&from={base_key}&amount={amount}"

        payload = {}
        headers = {"apikey": "yCb16Cp4WidBEpJZRyp1RyjKCmHZCCrQ"}

        response = requests.get(url, headers=headers)
        resp = json.loads(response.content)
        d = resp['result']
        message = f"Цена {amount} {base} в {quote} : {d}"

        return message
