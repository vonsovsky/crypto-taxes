"""
Entry file. Still some parts are WIP.
"""

from typing import List, Optional

import iso8601

from api import CryptoAPI
from config import REFERENCE_FIAT
from dto import Wallet, Order
from exchange import BinanceReader, CoinmateReader, GateIOReader, KucoinReader, PoloniexReader

REFRESH_DATA = False

wallet = Wallet()
api = CryptoAPI()


def calculate_profit(orders: List[Order], year: Optional[int] = None) -> float:
    if year is not None:
        begin_year = iso8601.parse_date(f"{year}-01-01 00:00:00")
        begin_next_year = iso8601.parse_date(f"{year + 1}-01-01 00:00:00")
        orders = filter(lambda x: begin_year <= x.filled < begin_next_year, orders)

    year_profit = 0

    for i, order in enumerate(orders):
        print(i, order)
        print(order.filled)
        if order.currency_from == REFERENCE_FIAT:
            wallet.buy(order.currency_to, count=order.count, price=order.unit_price, last_update=order.filled)
        else:
            total = wallet.get_currency_count(order.currency_from)
            avg_price = wallet.get_currency_avg_price(order.currency_from)

            currency_to_current_price = None
            if order.count_to is None:
                currency_to_current_price = api.get_currency_price_at(order.currency_to, order.filled)

            profit = wallet.convert(
                currency_from=order.currency_from,
                currency_to=order.currency_to,
                count_from=order.count,
                currency_from_current_price=order.unit_price,
                count_to=order.count_to,
                currency_to_current_price=currency_to_current_price
            )

            print(f"Selling {order.currency_from}. {order.count} out of {total}. "
                  f"Bought for avg price: {avg_price}, now for {order.unit_price} each")
            print(f"Profit: {profit}")

            year_profit += profit
        print()

    print()
    return year_profit


orders: List[Order] = []
readers = {
    "csv/coinmate_order_history.csv": CoinmateReader(),
    "csv/binance.csv": BinanceReader(),
    "csv/gate.io.csv": GateIOReader(),
    "csv/kucoin.csv": KucoinReader(),
    "csv/poloniex.csv": PoloniexReader(),
}

if REFRESH_DATA:
    for filename, inst_reader in readers.items():
        orders = inst_reader.read_file(filename)
        inst_reader.save(orders)

for inst_reader in readers.values():
    orders.extend(inst_reader.load())

orders.sort(key=lambda x: x.filled)

# add any wallet manually
wallet.buy("XRP", 800, 7.96)

# or try to add it by api for prices
price = api.get_currency_price_at("ETH", iso8601.parse_date("2017-12-21 14:49:43"))
print(price)
wallet.buy("ETH", 0.5, price)

profit = calculate_profit(orders, year=None)
print(f"Total taxable profit for year 2017-2021 is {profit} {REFERENCE_FIAT}")

print()
