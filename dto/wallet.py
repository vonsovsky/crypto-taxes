from datetime import datetime
from typing import Optional


class CurrencyWallet:
    def __init__(self, name):
        self.name = name
        self.count = 0.0
        self.avg_price = 0.0
        self.last_update = None

    def buy(self, count: float, price: float, last_update: Optional[datetime] = None):
        # update price by weighted average
        # 5 btc for 10000 in wallet, called 10 btc at 40000, should be 30000 now

        self.avg_price = (self.count * self.avg_price + count * price) / (self.count + count)
        self.count += count
        self.last_update = last_update

    def spend(self, count, current_price) -> float:
        """
        Spends money back and returns profit from its buying
        :return taxable profit in reference currency (CZK)
        """

        self.count -= count

        if self.count < -0.05:
            raise ValueError(f"Cannot go negative on {self.name}: {self.count}")

        profit = count * (current_price - self.avg_price)
        return profit

    def __repr__(self):
        return f"{self.count} {self.name} at average price {self.avg_price} per unit"


class Wallet:
    def __init__(self):
        self.currencies = dict()

    def convert(
            self,
            currency_from: str,
            currency_to: str,
            count_from: float,
            currency_from_current_price: float,
            count_to: Optional[float] = None,
            currency_to_current_price: Optional[float] = None
    ):
        """
        Converts two currencies - first one is deducted from the wallet and its finances are used to buy the second one
        :param currency_from: Currency to be spent
        :param currency_to: Currency to be bought
        :param count_from: How much currency to be spent
        :param currency_from_current_price: Currency to be spent actual price, will be used to calculate taxable profit
        :param count_to: How much currency to be bought
        :param currency_to_current_price: Currency to be bought actual price, will be used to count how much to buy
        :return: taxable profit from the conversion
        """

        # Destination currency could be empty, Origin currency cannot
        if currency_to not in self.currencies:
            self.currencies[currency_to] = CurrencyWallet(currency_to)

        currency_wallet1 = self.currencies.get(currency_from, CurrencyWallet(currency_from))
        currency_wallet2 = self.currencies.get(currency_to, CurrencyWallet(currency_to))

        sold_for = count_from * currency_from_current_price
        profit = currency_wallet1.spend(count_from, currency_from_current_price)

        if count_to is None:
            count_to = sold_for / currency_to_current_price
        if currency_to_current_price is None:
            currency_to_current_price = sold_for / count_to

        currency_wallet2.buy(count_to, currency_to_current_price)

        return profit

    def buy(self, currency: str, count: float, price: float, last_update: Optional[datetime] = None):
        if currency not in self.currencies:
            self.currencies[currency] = CurrencyWallet(currency)

        currency_wallet: CurrencyWallet = self.currencies[currency]
        currency_wallet.buy(count, price, last_update)

    def get_currency_count(self, currency: str):
        return self.currencies[currency].count

    def get_currency_avg_price(self, currency: str):
        return self.currencies[currency].avg_price

    def __repr__(self):
        string_builder = ""
        for currency, currency_wallet in self.currencies.items():
            string_builder += f"{currency}: {currency_wallet.count} in total with average " \
                              f"buying price {currency_wallet.avg_price}\n"

        return string_builder
