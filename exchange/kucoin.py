import csv

import iso8601

from api import CryptoAPI
from dto import Order
from .reader import Reader


class KucoinReader(Reader):
    PICKLE_FILENAME = "kucoin.pkl"
    EXCHANGE_NAME = "Kucoin"

    def __init__(self):
        self.api = CryptoAPI()

    def get_pickle_filename(self):
        return self.PICKLE_FILENAME

    def read_file(self, filename):
        fr = open(filename, "r")
        csvreader = csv.reader(fr, delimiter=",", quotechar='"')
        header = next(csvreader)

        records = []
        for row in csvreader:
            dt_row = dict((x, y) for x, y in zip(header, row))

            if dt_row["orderStatus"] != "done":
                continue

            filled = iso8601.parse_date(dt_row["orderCreatedAt"])
            if dt_row["side"] == "buy":
                currency_to, currency_from = dt_row["symbol"].split("-")
                count = float(dt_row["dealFunds"])
            elif dt_row["side"] == "sell":
                currency_from, currency_to = dt_row["symbol"].split("-")
                count = float(dt_row["dealSize"])
            else:
                raise ValueError(dt_row["side"])

            # price at order time, will be used to for taxing
            unit_price = self.api.get_currency_price_at(currency_from, filled)

            records.append(Order(
                filled=filled,
                currency_from=currency_from,
                currency_to=currency_to,
                count=count,
                unit_price=unit_price,
                exchange_name=self.EXCHANGE_NAME
            ))

        return records
