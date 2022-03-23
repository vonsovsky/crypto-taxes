import csv

import iso8601

from api import CryptoAPI
from dto import Order
from .reader import Reader


class PoloniexReader(Reader):
    PICKLE_FILENAME = "poloniex.pkl"
    EXCHANGE_NAME = "Poloniex"

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

            filled = iso8601.parse_date(dt_row["Date"])
            if dt_row["Type"] == "Buy":
                currency_to, currency_from = dt_row["Market"].split("/")
                count = float(dt_row["Total"])
            elif dt_row["Type"] == "Sell":
                currency_from, currency_to = dt_row["Market"].split("/")
                count = float(dt_row["Amount"])
            else:
                raise ValueError(dt_row["Type"])

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
