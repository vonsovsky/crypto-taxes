"""
Entry file. Mostly WIP.
"""

import iso8601

from dto import Wallet, Order
from exchange.coinmate import CoinmateReader
from config import REFERENCE_FIAT
from typing import List
from api import CryptoAPI

YEAR = 2021

wallet = Wallet()
api = CryptoAPI()


def calculate_profit_for_year(orders: List[Order], year: int) -> float:
    begin_year = iso8601.parse_date(f"{year}-01-01 00:00:00")
    begin_next_year = iso8601.parse_date(f"{year + 1}-01-01 00:00:00")

    orders_filtered = filter(lambda x: begin_year <= x.filled < begin_next_year, orders)
    year_profit = 0

    for i, order in enumerate(orders_filtered):
        print(i, order)

        if order.currency_from == REFERENCE_FIAT:
            wallet.buy(order.currency_to, count=order.count, price=order.unit_price, last_update=order.filled)
        else:
            total = wallet.get_currency_count(order.currency_from)
            avg_price = wallet.get_currency_avg_price(order.currency_from)

            currency_to_current_price = api.get_currency_price_at(order.currency_to, order.filled)
            profit = wallet.convert(
                currency_from=order.currency_from,
                currency_to=order.currency_to,
                count_from=order.count,
                currency_from_current_price=order.unit_price,
                currency_to_current_price=currency_to_current_price
            )

            print(f"Selling {order.currency_from}. {order.count} out of {total}. "
                  f"Bought for avg price: {avg_price}, now for {order.unit_price}")
            print(f"Profit: {profit}")

            year_profit += profit

    print()
    return year_profit


coinmate_reader = CoinmateReader()
#orders = coinmate_reader.read_file("coinmate_order_history.csv")
#coinmate_reader.save(orders)
orders: List[Order] = coinmate_reader.load()
orders.sort(key=lambda x: x.filled)

profit = calculate_profit_for_year(orders, YEAR)
print(f"Total taxable profit for year {YEAR} is {profit}")
