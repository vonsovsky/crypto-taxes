"""
Entry file. Mostly WIP.
"""

import iso8601

from dto import Wallet, Order
from exchange.coinmate import CoinmateReader
from config import REFERENCE_FIAT
from typing import List

coinmate_reader = CoinmateReader()
#orders = coinmate_reader.read_file("coinmate_order_history.csv")
#coinmate_reader.save(orders)
orders: List[Order] = coinmate_reader.load()

begin_2021 = iso8601.parse_date("2021-01-01 00:00:00")
begin_2022 = iso8601.parse_date("2022-01-01 00:00:00")

orders.sort(key=lambda x: x.filled)
orders = filter(lambda x: begin_2021 <= x.filled < begin_2022, orders)

wallet = Wallet()

# TODO WIP
for i, order in enumerate(orders):
    print(i, order)

    if order.currency_from == REFERENCE_FIAT:
        wallet.buy(order.currency_to, count=order.count, price=order.unit_price, last_update=order.filled)
    else:
        total = wallet.currencies[order.currency_from].count
        profit = wallet.convert(
            currency_from=order.currency_from,
            currency_to=order.currency_to,
            count_from=order.count,
            currency_from_current_price=order.unit_price,
            currency_to_current_price=1  # TODO real price
            # self.api.get_currency_price_at(mapping[order.currency_to], order.filled)
        )
        avg_price = wallet.currencies[order.currency_from].avg_price
        print(f"Selling {order.currency_from}. {order.count} out of {total}. "
              f"Bought for avg price: {avg_price}, now for {order.unit_price}")
        print(f"Profit: {profit}")
