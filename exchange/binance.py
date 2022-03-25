import csv

import iso8601

from api import CryptoAPI
from dto import Order
from .reader import Reader


class BinanceReader(Reader):
    PICKLE_FILENAME = "binance.pkl"
    EXCHANGE_NAME = "Binance"

    def __init__(self):
        self.api = CryptoAPI()

    def get_pickle_filename(self):
        return self.PICKLE_FILENAME

    def read_file(self, filename):
        fr = open(filename, "r")
        csvreader = csv.reader(fr, delimiter=";", quotechar='"')
        header = next(csvreader)

        records = []
        for row in csvreader:
            dt_row = dict((x, y) for x, y in zip(header, row))

            if dt_row["Status"] != "Successful":
                continue

            filled = iso8601.parse_date(dt_row["Date"])
            count_from, currency_from = dt_row["Sell"].split(" ")
            count_to, currency_to = dt_row["Buy"].split(" ")
            count_from = float(count_from)
            count_to = float(count_to)

            # price at order time, will be used to for taxing
            unit_price = self.api.get_currency_price_at(currency_from, filled)

            records.append(Order(
                filled=filled,
                currency_from=currency_from,
                currency_to=currency_to,
                count=count_from,
                count_to=count_to,
                unit_price=unit_price,
                exchange_name=self.EXCHANGE_NAME
            ))

        return records
