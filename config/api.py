from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import requests
from django.http import JsonResponse


def home(request):
    data = {"message": "hello from json response", "num": 12.2}
    return JsonResponse(data)


@dataclass
class ExchangeRate:
    date_: str
    from_: str
    to: str
    value: float

    @classmethod
    def from_response(cls, response: requests.Response):
        pure_response: dict = response.json()["Realtime Currency Exchange Rate"]
        from_ = pure_response["1. From_Currency Code"]
        to = pure_response["3. To_Currency Code"]
        value = pure_response["5. Exchange Rate"]
        date_ = pure_response["6. Last Refreshed"]
        return cls(from_=from_, to=to, value=value, date_=date_)

    def __eq__(self, other: ExchangeRate):
        return self.value == other.value


ExchangeRates = list[ExchangeRate]


class ExchangeRatesHistory:
    @classmethod
    def add(cls, instance: ExchangeRate):
        """We woud like to add ExchangeRates instances if it is not last duplicated"""
        cls.write_in_history(instance)

    @classmethod
    def as_dict(cls):
        """Main representation interface"""

        return {"results": [asdict(er) for er in cls._history]}

    def write_in_history(instan):

        FILENAME = "history.json"
        add_new_line = True
        instance_dict = {"from_": instan.from_, " to": instan.to, "value": instan.value}

        for line in ExchangeRatesHistory.read_lines(FILENAME):
            if line != "\n":
                if json.loads(line) == instance_dict:
                    add_new_line = False
        if add_new_line is True:
            with open(FILENAME, "a") as json_file:

                print(instance_dict)
                json_file.write("\n")
                json.dump(instance_dict, json_file)
                json_file.close()

    def read_lines(FILENAME):
        with open(FILENAME) as json_file:
            while True:
                line = json_file.readline()
                if not line:
                    break
                yield line


def btc_usd(request=None):
    # def btc_usd(request): розкоментити
    # NOTE: Connect to the external exchange rates API
    API_KEY = "82I46WMYT3C7EX3J"
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency=BTC&to_currency=USD&apikey={API_KEY}"
    )
    response = requests.get(url)
    exchange_rate = ExchangeRate.from_response(response)
    ExchangeRatesHistory.add(exchange_rate)
    # return JsonResponse(asdict(exchange_rate)) розкоментити


def history(request):
    return JsonResponse(ExchangeRatesHistory.as_dict())


# закоментити
if __name__ == "__main__":
    print("1")
    btc_usd()
