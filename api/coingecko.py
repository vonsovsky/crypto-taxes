from datetime import datetime

from pycoingecko import CoinGeckoAPI
from config import REFERENCE_FIAT


MAPPING = {
    REFERENCE_FIAT: REFERENCE_FIAT,
    "BTC": "bitcoin",
    "LTC": "litecoin",
    "ETH": "ethereum",
    "ADA": "cardano",
    "XRP": "ripple",
    "DAI": "dai",
    "DASH": "dash",
}


class CryptoAPI:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_currency_price_at(self, currency: str, date_at: datetime):
        """
        Get currency price at datetime specified in UTC+0

        :param currency code of currency
        :param date_at time of transaction to evaluate price
        """

        if currency == REFERENCE_FIAT:
            return 1

        currency_name = MAPPING[currency]
        date_at = int(datetime.timestamp(date_at))
        hist = self.cg.get_coin_market_chart_range_by_id(
            currency_name, vs_currency=REFERENCE_FIAT, from_timestamp=date_at, to_timestamp=date_at + 3600)

        measured_at = datetime.fromtimestamp(hist["prices"][0][0] / 1000)
        print(measured_at)
        return hist["prices"][0][1]
