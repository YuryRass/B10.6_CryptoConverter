import requests
import json

values = {
    'доллар': 'USD',
    'биткоин': 'BTC', 
    'эфириум': 'ETH',
    'рубль': 'RUB',
    'евро': 'USD',
    'юань': 'CNY',
    'иена': 'JPY',
    'вона': 'KRW',
    'фунт': 'GBP',
    'франк': 'CHF',
    'крона': 'CZK',
    'рупия': 'INR',
    'лира': 'TRY',
    'шекель': 'ILS',
    'рэнд': 'ZAR'
}

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base_, quote_, amount_):
        try:
            base, quote = values[base_], values[quote_]
            if base == quote:
                raise APIException('Имена валют принимают одинаковые значения')
            amount = float(amount_)
            if amount < 0:
                raise ValueError
        except APIException as e:
            return f'{e}'
        except KeyError:
            return 'Данные значения не входят в список доступных валют\n \
(Введите /values - для вывода доступных денежных валют)'
        except ValueError:
            return 'Количество валюты принимает положительное числовое значение'

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}')
        data = json.loads(r.content)
        sum = float(data[quote]) * amount
        return f'{amount} {base_} = {sum} {quote_}'

