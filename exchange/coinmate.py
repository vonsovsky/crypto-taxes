import csv

import iso8601

from api import CryptoAPI
from dto import Order
from .reader import Reader


class CoinmateReader(Reader):
    PICKLE_FILENAME = "coinmate.pkl"
    EXCHANGE_NAME = "Coinmate"

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
            filled = iso8601.parse_date(dt_row["DATE FILLED"])
            if dt_row["TYPE"] == "BUY" or dt_row["TYPE"] == "QUICK BUY":
                currency_to, currency_from = dt_row["PAIR"].split("_")

                if len(dt_row["ORIG. SIZE"]) > 0:
                    count = float(dt_row["ORIG. SIZE"])
                    unit_price = float(dt_row["ORDER TOTAL"]) / count
                else:
                    price_from = self.api.get_currency_price_at(currency_from, filled)
                    unit_price = self.api.get_currency_price_at(currency_to, filled)
                    count = price_from * float(dt_row["ORDER TOTAL"]) / unit_price
            elif dt_row["TYPE"] == "SELL" or dt_row["TYPE"] == "QUICK SELL":
                currency_from, currency_to = dt_row["PAIR"].split("_")

                unit_price = self.api.get_currency_price_at(currency_from, filled)
                count = float(dt_row["ORIG. SIZE"])
            else:
                raise ValueError(dt_row["TYPE"])

            records.append(Order(
                filled=filled,
                currency_from=currency_from,
                currency_to=currency_to,
                count=count,
                unit_price=unit_price,
                exchange_name=self.EXCHANGE_NAME
            ))

        return records
