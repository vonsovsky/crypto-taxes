from datetime import datetime
from time import sleep

from pycoingecko import CoinGeckoAPI
from config import REFERENCE_FIAT


# some value are flagged as shitcoin
# will never be reused again, nothing will be bought for it, so it's not necessary to find out the price
MAPPING = {
    REFERENCE_FIAT: REFERENCE_FIAT,
    "BTC": "bitcoin",
    "LTC": "litecoin",
    "ETH": "ethereum",
    "ADA": "cardano",
    "XRP": "ripple",
    "DAI": "dai",
    "DASH": "dash",
    "XVG": "verge",
    "SOL": "solana",
    "SHIB": "shiba-inu",
    "BNB": "binance-coin",
    "USDT": "tether",
    "USDC": "usd-coin",
    "SAMO": "samoyedcoin",
    "STARL": "starlink",
    "KCS": "kucoin-shares",
    "RMRK": "rmrk",
    "ERG": "ergo",
    "DOGE": "dogecoin",
    "XLM": "stellar",
    "STR": "stellar",
    "DOT": "polkadot",
    "TRX": "tron",
    "AAVE": "aave",
    "ELON": "shitcoin",
    "BABYDOGE": "shitcoin",
    "AKITA": "shitcoin",
    "ETHBEAR": "shitcoin",
    "LINKBEAR": "shitcoin",
    "MAID": "shitcoin",
    "BURST": "shitcoin",
}


class CryptoAPI:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_currency_price_at(self, currency: str, date_at: datetime, allow_range: int = 5000):
        """
        Get currency price at datetime specified in UTC+0

        :param currency code of currency
        :param date_at time of transaction to evaluate price
        :param allow_range add some tolerance as API might not have data for the exact given time
        """

        if currency == REFERENCE_FIAT or MAPPING[currency] == "shitcoin":
            return 1

        currency_name = MAPPING[currency]
        date_at = int(datetime.timestamp(date_at))
        sleep(1)
        hist = self.cg.get_coin_market_chart_range_by_id(
            currency_name, vs_currency=REFERENCE_FIAT, from_timestamp=date_at, to_timestamp=date_at + allow_range)

        measured_at = datetime.fromtimestamp(hist["prices"][0][0] / 1000)
        print(measured_at)
        return hist["prices"][0][1]

    def get_avg_price_over_time(self, currency: str, from_dt: datetime, to_dt: datetime):
        currency_name = MAPPING[currency]
        from_dt = int(datetime.timestamp(from_dt))
        to_dt = int(datetime.timestamp(to_dt))
        sleep(1)
        hist = self.cg.get_coin_market_chart_range_by_id(
            currency_name, vs_currency=REFERENCE_FIAT, from_timestamp=from_dt, to_timestamp=to_dt + 5000)

        suma = 0
        for i in range(len(hist["prices"])):
            suma += hist["prices"][i][1]

        return suma / len(hist["prices"])
